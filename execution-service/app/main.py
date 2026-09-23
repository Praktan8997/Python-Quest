import sys
import subprocess
import tempfile
import os
import time
from dotenv import load_dotenv
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load .env for local development
load_dotenv()

app = FastAPI(title="Python Quest Isolated Execution Service")

# CORS — restrict to backend domain in production; allow all in local dev
_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
if _raw_origins == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestCase(BaseModel):
    input: Optional[str] = ""
    expected_output: str

class ExecutionRequest(BaseModel):
    code: str
    timeout: Optional[float] = 5.0
    test_cases: Optional[List[TestCase]] = None

class TestCaseResult(BaseModel):
    input: str
    expected_output: str
    actual_output: str
    passed: bool

class ExecutionResponse(BaseModel):
    success: bool
    stdout: str
    stderr: str
    execution_time_ms: float
    error: Optional[str] = None
    all_tests_passed: Optional[bool] = None
    test_results: Optional[List[TestCaseResult]] = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "execution-service"}

@app.post("/run", response_model=ExecutionResponse)
def run_code(req: ExecutionRequest):
    # Create temp script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
        tmp.write(req.code)
        tmp_path = tmp.name

    try:
        start_time = time.time()

        # Simple run without test cases
        if not req.test_cases:
            try:
                proc = subprocess.run(
                    [sys.executable, tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=req.timeout
                )
                exec_time = round((time.time() - start_time) * 1000, 2)
                stdout = proc.stdout.strip()
                stderr = proc.stderr.strip()
                return ExecutionResponse(
                    success=(proc.returncode == 0),
                    stdout=stdout,
                    stderr=stderr,
                    execution_time_ms=exec_time,
                    error=stderr if proc.returncode != 0 else None
                )
            except subprocess.TimeoutExpired:
                exec_time = round((time.time() - start_time) * 1000, 2)
                return ExecutionResponse(
                    success=False,
                    stdout="",
                    stderr="Execution timed out.",
                    execution_time_ms=exec_time,
                    error="Time Limit Exceeded"
                )

        # Run with test cases
        test_results = []
        all_passed = True
        overall_stdout = ""
        overall_stderr = ""

        for tc in req.test_cases:
            tc_input = tc.input or ""
            try:
                proc = subprocess.run(
                    [sys.executable, tmp_path],
                    input=tc_input,
                    capture_output=True,
                    text=True,
                    timeout=req.timeout
                )
                stdout = proc.stdout.strip()
                stderr = proc.stderr.strip()
                expected = tc.expected_output.strip()

                passed = (proc.returncode == 0) and (stdout == expected)
                if not passed:
                    all_passed = False

                test_results.append(TestCaseResult(
                    input=tc_input,
                    expected_output=expected,
                    actual_output=stdout if proc.returncode == 0 else (stderr or "Error"),
                    passed=passed
                ))
                if stdout:
                    overall_stdout += stdout + "\n"
                if stderr:
                    overall_stderr += stderr + "\n"

            except subprocess.TimeoutExpired:
                all_passed = False
                test_results.append(TestCaseResult(
                    input=tc_input,
                    expected_output=tc.expected_output,
                    actual_output="Time Limit Exceeded",
                    passed=False
                ))

        exec_time = round((time.time() - start_time) * 1000, 2)
        return ExecutionResponse(
            success=all_passed,
            stdout=overall_stdout.strip(),
            stderr=overall_stderr.strip(),
            execution_time_ms=exec_time,
            all_tests_passed=all_passed,
            test_results=test_results
        )

    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
