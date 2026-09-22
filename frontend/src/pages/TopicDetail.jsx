import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { topicService, challengeService, quizService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { BookOpen, Code, HelpCircle, Play, CheckCircle2, XCircle, ArrowLeft, Zap, RefreshCw, Lightbulb, History, Check, ShieldCheck } from 'lucide-react';

export const TopicDetail = () => {
  const { topicId } = useParams();
  const { reloadProgress } = useAuth();

  const [topic, setTopic] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [challenges, setChallenges] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [activeTab, setActiveTab] = useState('learn'); // 'learn', 'challenge', 'quiz'

  // Code editor state
  const [currentChallenge, setCurrentChallenge] = useState(null);
  const [code, setCode] = useState('');
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState(null);
  const [showHint, setShowHint] = useState(false);

  // Quiz state
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizSubmitting, setQuizSubmitting] = useState(false);
  const [quizResult, setQuizResult] = useState(null);
  const [quizAttempts, setQuizAttempts] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTopicDetails = async () => {
      try {
        setLoading(true);
        const [topRes, lesRes, chalRes, qzRes] = await Promise.all([
          topicService.getTopicById(topicId),
          topicService.getLessons(topicId),
          topicService.getChallenges(topicId),
          topicService.getQuizzes(topicId)
        ]);

        setTopic(topRes.data);
        setLessons(lesRes.data);
        setChallenges(chalRes.data);
        setQuizzes(qzRes.data);

        if (chalRes.data.length > 0) {
          const firstChal = chalRes.data[0];
          setCurrentChallenge(firstChal);
          setCode(firstChal.starter_code || '# Write your Python code here\n');
        }

        if (qzRes.data.length > 0) {
          const qz = qzRes.data[0];
          setCurrentQuiz(qz);
          try {
            const attRes = await quizService.getAttempts(qz.id);
            setQuizAttempts(attRes.data);
          } catch (e) {
            console.error(e);
          }
        }
      } catch (err) {
        console.error('Error fetching topic detail', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTopicDetails();
  }, [topicId]);

  const selectChallenge = (chal) => {
    setCurrentChallenge(chal);
    setCode(chal.starter_code || '');
    setSubmitResult(null);
    setShowHint(false);
  };

  const handleRunCode = async () => {
    if (!currentChallenge) return;
    setRunning(true);
    setSubmitResult(null);

    try {
      const res = await challengeService.runCode(currentChallenge.id, code);
      setSubmitResult({
        ...res.data,
        is_dry_run: true
      });
    } catch (err) {
      setSubmitResult({
        success: false,
        passed: false,
        stdout: '',
        stderr: err.response?.data?.detail || 'Error running code.'
      });
    } finally {
      setRunning(false);
    }
  };

  const handleSubmitCode = async () => {
    if (!currentChallenge) return;
    setSubmitting(true);
    setSubmitResult(null);

    try {
      const submitFn = challengeService.submitSolution || challengeService.submitChallenge;
      const res = await submitFn(currentChallenge.id, code);
      setSubmitResult({
        ...res.data,
        is_dry_run: false
      });
      if (res.data.passed) {
        reloadProgress();
      }
    } catch (err) {
      console.error('Error submitting solution:', err);
      setSubmitResult({
        success: false,
        passed: false,
        stdout: '',
        stderr: err.response?.data?.detail || err.message || 'Error submitting solution.'
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleOptionSelect = (questionId, optionId) => {
    setQuizAnswers((prev) => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  const handleTextAnswer = (questionId, text) => {
    setQuizAnswers((prev) => ({
      ...prev,
      [questionId]: text
    }));
  };

  const handleQuizSubmit = async () => {
    if (!currentQuiz) return;
    setQuizSubmitting(true);
    setQuizResult(null);

    const answersPayload = Object.entries(quizAnswers).map(([qId, answer]) => {
      const question = currentQuiz.questions?.find(q => q.id === parseInt(qId));
      const qType = question?.question_type || 'multiple_choice';
      const isTextQuestion = ['fill_in_blank', 'code_output'].includes(qType);

      return {
        question_id: parseInt(qId),
        selected_option_id: isTextQuestion ? 0 : (typeof answer === 'number' ? answer : 0),
        answer_text: isTextQuestion ? String(answer) : undefined
      };
    });

    try {
      const res = await quizService.submitQuiz(currentQuiz.id, answersPayload);
      setQuizResult(res.data);
      if (res.data.passed) {
        reloadProgress();
      }
      const attRes = await quizService.getAttempts(currentQuiz.id);
      setQuizAttempts(attRes.data);
    } catch (err) {
      console.error('Quiz submit failed:', err);
    } finally {
      setQuizSubmitting(false);
    }
  };

  if (loading || !topic) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <RefreshCw className="w-8 h-8 text-[#663af3] animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8 animate-pq-fade-up">
      {/* Top Header & Breadcrumb */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 border-b border-[rgba(186,215,247,0.12)] pb-6">
        <div>
          <Link to="/explore" className="inline-flex items-center gap-1.5 text-xs text-[#8AA4C4] hover:text-[#F0F6FF] mb-2 transition-colors">
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Curriculum
          </Link>
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs uppercase tracking-wider text-[#8AA4C4] bg-[rgba(186,214,247,0.04)] px-3 py-1 rounded-badge border border-[rgba(186,215,247,0.14)]">
              {topic.level_title}
            </span>
            <h1 className="text-3xl sm:text-5xl font-heading font-medium authkit-heading-gradient tracking-tight">{topic.title}</h1>
          </div>
        </div>

        {/* Tab Selection AuthKit Pills */}
        <div className="flex items-center gap-1.5 bg-[rgba(186,214,247,0.03)] border border-[rgba(186,215,247,0.12)] p-1.5 rounded-full backdrop-blur-xl">
          <button
            onClick={() => setActiveTab('learn')}
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all flex items-center gap-2 ${
              activeTab === 'learn'
                ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)] shadow-sm'
                : 'text-[#8AA4C4] hover:text-[#F0F6FF]'
            }`}
          >
            <BookOpen className="w-4 h-4 text-[#8AA4C4]" /> 1. Learn
          </button>
          <button
            onClick={() => setActiveTab('challenge')}
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all flex items-center gap-2 ${
              activeTab === 'challenge'
                ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)] shadow-sm'
                : 'text-[#8AA4C4] hover:text-[#F0F6FF]'
            }`}
          >
            <Code className="w-4 h-4 text-[#8AA4C4]" /> 2. Challenge ({challenges.length})
          </button>
          <button
            onClick={() => setActiveTab('quiz')}
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all flex items-center gap-2 ${
              activeTab === 'quiz'
                ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)] shadow-sm'
                : 'text-[#8AA4C4] hover:text-[#F0F6FF]'
            }`}
          >
            <HelpCircle className="w-4 h-4 text-[#8AA4C4]" /> 3. Quiz
          </button>
        </div>
      </div>

      {/* TAB 1: LEARN */}
      {activeTab === 'learn' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            {lessons.map((les) => (
              <div key={les.id} className="authkit-glass-card p-8 space-y-4 rounded-card">
                <h3 className="text-xl font-heading font-semibold text-[#F0F6FF] flex items-center gap-2.5">
                  <BookOpen className="w-5 h-5 text-[#8AA4C4]" /> {les.title}
                </h3>
                <div className="text-[#C8DCF5]/90 text-sm leading-relaxed whitespace-pre-line font-sans">
                  {les.content}
                </div>
              </div>
            ))}
          </div>

          <div className="space-y-6">
            {lessons.map((les) => (
              les.code_example && (
                <div key={`ex-${les.id}`} className="authkit-glass-card overflow-hidden rounded-card">
                  <div className="bg-[rgba(186,214,247,0.03)] px-6 py-3.5 border-b border-[rgba(186,215,247,0.12)] flex items-center justify-between">
                    <span className="text-xs font-mono font-medium text-[#8AA4C4] flex items-center gap-2">
                      <Code className="w-4 h-4 text-[#8AA4C4]" /> Code Sample
                    </span>
                    <button
                      onClick={() => {
                        setCode(les.code_example);
                        setActiveTab('challenge');
                      }}
                      className="text-xs font-semibold text-[#F0F6FF] hover:text-[#663af3] flex items-center gap-1.5 transition-colors"
                    >
                      <Play className="w-3.5 h-3.5 text-[#663af3] fill-[#663af3]" /> Try in Editor →
                    </button>
                  </div>
                  <pre className="p-6 font-mono text-xs bg-[#090b17] text-[#C8DCF5] overflow-x-auto">
                    <code>{les.code_example}</code>
                  </pre>
                </div>
              )
            ))}

            <div className="authkit-glass-card p-8 text-center space-y-4 rounded-card">
              <h4 className="text-lg font-heading font-semibold text-[#F0F6FF]">Understood the Concept?</h4>
              <p className="text-xs text-[#8AA4C4] max-w-md mx-auto">Execute your code solution in our isolated Python sandbox!</p>
              <button
                onClick={() => setActiveTab('challenge')}
                className="authkit-btn-violet px-6 py-2.5 text-xs font-semibold rounded-md shadow-[0_0_20px_rgba(102,58,243,0.4)]"
              >
                Go to Coding Challenge →
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: CODE CHALLENGE & EDITOR */}
      {activeTab === 'challenge' && (
        <div className="space-y-6">
          {/* Challenge Selector Pills */}
          {challenges.length > 1 && (
            <div className="flex items-center gap-2 bg-[rgba(186,214,247,0.03)] p-2 rounded-full border border-[rgba(186,215,247,0.12)]">
              <span className="text-xs font-mono text-[#526884] px-3">Challenges:</span>
              {challenges.map((c, idx) => (
                <button
                  key={c.id}
                  onClick={() => selectChallenge(c)}
                  className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
                    currentChallenge?.id === c.id
                      ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)]'
                      : 'text-[#8AA4C4] hover:text-[#F0F6FF]'
                  }`}
                >
                  Challenge {idx + 1}: {c.title}
                </button>
              ))}
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 min-h-[600px]">
            {/* Challenge Description (5 cols) */}
            <div className="lg:col-span-5 authkit-glass-card p-8 flex flex-col justify-between space-y-6 rounded-card">
              {currentChallenge ? (
                <div className="space-y-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono uppercase tracking-wider text-[#8AA4C4] bg-[rgba(186,214,247,0.04)] px-3 py-1 rounded-badge border border-[rgba(186,215,247,0.14)]">
                      Difficulty: {currentChallenge.difficulty}
                    </span>
                    <span className="text-xs font-mono font-bold text-[#F0F6FF] flex items-center gap-1">
                      <Zap className="w-4 h-4 text-[#663af3] fill-[#663af3]" /> +{currentChallenge.xp_reward} XP
                    </span>
                  </div>

                  <h2 className="text-2xl font-heading font-semibold text-[#F0F6FF]">{currentChallenge.title}</h2>
                  <p className="text-[#C8DCF5]/90 text-sm leading-relaxed whitespace-pre-line font-sans">
                    {currentChallenge.description}
                  </p>

                  {currentChallenge.hint && (
                    <div className="pt-2">
                      <button
                        onClick={() => setShowHint(!showHint)}
                        className="inline-flex items-center gap-1.5 text-xs text-[#F0F6FF] font-medium bg-[rgba(186,214,247,0.06)] hover:bg-[rgba(186,214,247,0.1)] px-3.5 py-1.5 rounded-badge border border-[rgba(186,215,247,0.14)] transition-all"
                      >
                        <Lightbulb className="w-3.5 h-3.5 text-[#663af3]" />
                        {showHint ? 'Hide Hint' : '💡 Need a Hint?'}
                      </button>
                      {showHint && (
                        <div className="mt-3 bg-[#090b17] border border-[rgba(186,215,247,0.14)] p-4 rounded-card text-xs text-[#8AA4C4] leading-relaxed font-sans">
                          <strong className="text-[#F0F6FF]">Hint:</strong> {currentChallenge.hint}
                        </div>
                      )}
                    </div>
                  )}

                  {submitResult && submitResult.passed && !submitResult.is_dry_run && currentChallenge.solution_explanation && (
                    <div className="bg-[rgba(186,214,247,0.04)] border border-[rgba(186,215,247,0.18)] p-4 rounded-card text-xs text-[#C8DCF5] space-y-1">
                      <strong className="text-[#F0F6FF] block font-heading font-semibold text-sm">🎉 Solution Explanation:</strong>
                      <p className="leading-relaxed text-[#8AA4C4] font-sans">{currentChallenge.solution_explanation}</p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-[#526884] text-sm">No challenge available for this topic.</p>
              )}

              {/* Test Results Output Box */}
              {submitResult && (
                <div
                  className={`p-5 rounded-card border space-y-2 text-xs font-sans ${
                    submitResult.passed
                      ? 'bg-[rgba(186,214,247,0.05)] border-[rgba(186,215,247,0.2)] text-[#F0F6FF]'
                      : 'bg-red-500/10 border-red-500/30 text-red-300'
                  }`}
                >
                  <div className="flex items-center justify-between font-bold text-sm">
                    <span className="flex items-center gap-2">
                      {submitResult.passed ? <CheckCircle2 className="w-4 h-4 text-[#F0F6FF]" /> : <XCircle className="w-4 h-4 text-red-400" />}
                      {submitResult.passed
                        ? (submitResult.is_dry_run ? 'Dry Run Passed! (Submit to earn XP)' : 'Challenge Solved! Correct 🎉')
                        : 'Tests Failed — Keep Trying!'}
                    </span>
                    {!submitResult.is_dry_run && submitResult.xp_gained > 0 && (
                      <span className="text-[#663af3] font-bold">+ {submitResult.xp_gained} XP</span>
                    )}
                  </div>

                  {submitResult.stdout && (
                    <div className="mt-2 bg-[#090b17] p-3 rounded-badge font-mono text-[#C8DCF5] text-xs border border-[rgba(186,215,247,0.12)]">
                      <strong className="text-[#8AA4C4]">Output:</strong>
                      <pre className="whitespace-pre-wrap mt-1">{submitResult.stdout}</pre>
                    </div>
                  )}

                  {submitResult.stderr && (
                    <div className="mt-2 bg-[#090b17] p-3 rounded-badge font-mono text-red-400 text-xs border border-red-500/20">
                      <strong>Error Log:</strong>
                      <pre className="whitespace-pre-wrap mt-1">{submitResult.stderr}</pre>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Monaco Editor Container in Deep Midnight Frame (7 cols) */}
            <div className="lg:col-span-7 bg-[#090b17] border border-[rgba(186,215,247,0.14)] rounded-card overflow-hidden flex flex-col shadow-glass-elevation">
              <div className="bg-[rgba(186,214,247,0.03)] px-6 py-3.5 border-b border-[rgba(186,215,247,0.12)] flex items-center justify-between">
                <span className="text-xs font-mono text-[#8AA4C4] flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#663af3]" /> main.py
                </span>
                
                <div className="flex items-center gap-3">
                  <button
                    onClick={handleRunCode}
                    disabled={running || submitting}
                    className="authkit-btn-ghost px-4 py-1.5 text-xs font-medium flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {running ? 'Testing...' : <><Play className="w-3.5 h-3.5 text-[#8AA4C4]" /> Run Test</>}
                  </button>
                  <button
                    onClick={handleSubmitCode}
                    disabled={running || submitting}
                    className="authkit-btn-violet px-5 py-1.5 text-xs font-semibold rounded-md shadow-[0_0_15px_rgba(102,58,243,0.4)] flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {submitting ? 'Submitting...' : <><Check className="w-4 h-4" /> Submit Solution</>}
                  </button>
                </div>
              </div>

              <div className="flex-1 min-h-[460px] p-2 bg-[#090b17]">
                <Editor
                  height="450px"
                  defaultLanguage="python"
                  theme="vs-dark"
                  value={code}
                  onChange={(val) => setCode(val || '')}
                  options={{
                    fontSize: 14,
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    lineNumbers: 'on',
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: QUIZ */}
      {activeTab === 'quiz' && (
        <div className="max-w-3xl mx-auto space-y-6">
          {currentQuiz && currentQuiz.questions.length > 0 ? (
            <div className="authkit-glass-card p-8 sm:p-10 space-y-8 rounded-card">
              <div className="flex items-center justify-between border-b border-[rgba(186,215,247,0.12)] pb-5">
                <div>
                  <h2 className="text-2xl font-heading font-semibold text-[#F0F6FF]">{currentQuiz.title}</h2>
                  <p className="text-xs text-[#8AA4C4] font-sans mt-1">Answer all {currentQuiz.questions.length} questions to complete the module quiz!</p>
                </div>
                <span className="text-xs font-mono text-[#F0F6FF] bg-[rgba(186,214,247,0.06)] px-3.5 py-1.5 rounded-badge border border-[rgba(186,215,247,0.14)]">
                  +{currentQuiz.xp_reward} XP
                </span>
              </div>

              {/* Question List */}
              <div className="space-y-8">
                {currentQuiz.questions.map((q, idx) => {
                  const qType = q.question_type || 'multiple_choice';
                  const currentAnswer = quizAnswers[q.id];

                  return (
                    <div key={q.id} className="space-y-4 bg-[rgba(186,214,247,0.02)] p-6 rounded-card border border-[rgba(186,215,247,0.12)]">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-base font-heading font-semibold text-[#F0F6FF] flex items-center gap-3">
                          <span className="w-7 h-7 rounded-circle bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.2)] flex items-center justify-center text-xs shrink-0 font-bold font-mono">
                            {idx + 1}
                          </span>
                          {q.question_text}
                        </h3>
                        {qType !== 'multiple_choice' && (
                          <span className="text-xs font-mono bg-[rgba(186,214,247,0.04)] px-3 py-1 rounded-badge text-[#8AA4C4] capitalize border border-[rgba(186,215,247,0.12)]">
                            {qType.replace(/_/g, ' ')}
                          </span>
                        )}
                      </div>

                      {/* Multiple Choice */}
                      {qType === 'multiple_choice' && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pl-9">
                          {q.options && q.options.map((opt) => {
                            const isSelected = currentAnswer === opt.id;
                            return (
                              <button
                                key={opt.id}
                                onClick={() => handleOptionSelect(q.id, opt.id)}
                                className={`p-4 rounded-badge border text-left text-xs font-medium transition-all ${
                                  isSelected
                                    ? 'bg-[rgba(102,58,243,0.2)] border-[#663af3] text-[#F0F6FF] shadow-[0_0_15px_rgba(102,58,243,0.3)]'
                                    : 'bg-[rgba(186,214,247,0.03)] border-[rgba(186,215,247,0.12)] text-[#8AA4C4] hover:bg-[rgba(186,214,247,0.06)]'
                                }`}
                              >
                                {opt.option_text}
                              </button>
                            );
                          })}
                        </div>
                      )}

                      {/* True / False */}
                      {qType === 'true_false' && (
                        <div className="grid grid-cols-2 gap-4 pl-9">
                          {q.options && q.options.length > 0 ? (
                            q.options.map((opt) => {
                              const isSelected = currentAnswer === opt.id;
                              return (
                                <button
                                  key={opt.id}
                                  onClick={() => handleOptionSelect(q.id, opt.id)}
                                  className={`p-4 rounded-badge border text-center text-xs font-medium transition-all ${
                                    isSelected
                                      ? 'bg-[rgba(102,58,243,0.2)] border-[#663af3] text-[#F0F6FF] shadow-[0_0_15px_rgba(102,58,243,0.3)]'
                                      : 'bg-[rgba(186,214,247,0.03)] border-[rgba(186,215,247,0.12)] text-[#8AA4C4] hover:bg-[rgba(186,214,247,0.06)]'
                                  }`}
                                >
                                  {opt.option_text}
                                </button>
                              );
                            })
                          ) : (
                            <>
                              <button
                                onClick={() => handleOptionSelect(q.id, 1)}
                                className={`p-4 rounded-badge border text-center text-xs font-medium transition-all ${
                                  currentAnswer === 1
                                    ? 'bg-[rgba(102,58,243,0.2)] border-[#663af3] text-[#F0F6FF] shadow-[0_0_15px_rgba(102,58,243,0.3)]'
                                    : 'bg-[rgba(186,214,247,0.03)] border-[rgba(186,215,247,0.12)] text-[#8AA4C4] hover:bg-[rgba(186,214,247,0.06)]'
                                }`}
                              >
                                True
                              </button>
                              <button
                                onClick={() => handleOptionSelect(q.id, 2)}
                                className={`p-4 rounded-badge border text-center text-xs font-medium transition-all ${
                                  currentAnswer === 2
                                    ? 'bg-[rgba(102,58,243,0.2)] border-[#663af3] text-[#F0F6FF] shadow-[0_0_15px_rgba(102,58,243,0.3)]'
                                    : 'bg-[rgba(186,214,247,0.03)] border-[rgba(186,215,247,0.12)] text-[#8AA4C4] hover:bg-[rgba(186,214,247,0.06)]'
                                }`}
                              >
                                False
                              </button>
                            </>
                          )}
                        </div>
                      )}

                      {/* Fill in the blank / Code output */}
                      {(qType === 'fill_in_blank' || qType === 'code_output') && (
                        <div className="space-y-3 pl-9">
                          <textarea
                            value={typeof currentAnswer === 'string' ? currentAnswer : ''}
                            onChange={(e) => handleTextAnswer(q.id, e.target.value)}
                            placeholder="Type your answer here..."
                            className="w-full p-4 rounded-badge bg-[#090b17] border border-[rgba(186,215,247,0.14)] text-[#F0F6FF] font-mono text-xs resize-y min-h-[90px] focus:outline-none focus:border-[#663af3] transition-colors"
                          />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Submit Quiz Button */}
              <div className="pt-4 border-t border-[rgba(186,215,247,0.12)] flex justify-end">
                <button
                  onClick={handleQuizSubmit}
                  disabled={quizSubmitting || Object.keys(quizAnswers).length === 0}
                  className="authkit-btn-violet px-8 py-3 text-xs font-semibold rounded-md shadow-[0_0_20px_rgba(102,58,243,0.4)] disabled:opacity-50"
                >
                  {quizSubmitting ? 'Grading...' : 'Submit Quiz'}
                </button>
              </div>

              {/* Quiz Results Feedback */}
              {quizResult && (
                <div
                  className={`p-8 rounded-card border space-y-5 ${
                    quizResult.passed
                      ? 'bg-[rgba(186,214,247,0.04)] border-[rgba(186,215,247,0.2)] text-[#F0F6FF]'
                      : 'bg-red-500/10 border-red-500/30 text-red-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <h3 className="text-xl font-heading font-semibold flex items-center gap-2">
                      {quizResult.passed ? <CheckCircle2 className="w-5 h-5 text-[#663af3]" /> : <XCircle className="w-5 h-5 text-red-400" />}
                      {quizResult.passed ? 'Quiz Passed!' : 'Quiz Needs Practice'}
                    </h3>
                    <span className="text-sm font-mono font-bold">
                      Score: {quizResult.score} / {quizResult.total_questions} ({quizResult.percentage}%)
                    </span>
                  </div>

                  {quizResult.xp_gained > 0 && (
                    <div className="p-4 bg-[#663af3]/15 border border-[#663af3]/30 rounded-badge text-[#F0F6FF] text-xs font-bold flex items-center gap-2">
                      <Zap className="w-4 h-4 text-[#663af3] fill-[#663af3]" /> You earned +{quizResult.xp_gained} XP!
                    </div>
                  )}

                  <div className="space-y-3 pt-2">
                    {quizResult.feedback.map((fb, i) => (
                      <div key={fb.question_id} className="p-4 rounded-badge bg-[#090b17] text-xs space-y-1 border border-[rgba(186,215,247,0.12)]">
                        <div className="font-semibold flex items-center gap-2">
                          {fb.is_correct ? (
                            <span className="text-[#8AA4C4]">✓ Question {i + 1} Correct</span>
                          ) : (
                            <span className="text-red-400">✕ Question {i + 1} Incorrect</span>
                          )}
                        </div>
                        {fb.explanation && <p className="text-[#526884] italic mt-1">{fb.explanation}</p>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Attempts History */}
              {quizAttempts.length > 0 && (
                <div className="border-t border-[rgba(186,215,247,0.12)] pt-6 space-y-4">
                  <h4 className="font-eyebrow text-xs text-[#8AA4C4] uppercase tracking-wider flex items-center gap-2">
                    <History className="w-4 h-4 text-[#8AA4C4]" /> PREVIOUS QUIZ ATTEMPTS
                  </h4>
                  <div className="space-y-2">
                    {quizAttempts.map((att) => (
                      <div key={att.id} className="flex items-center justify-between p-4 rounded-badge bg-[rgba(186,214,247,0.02)] border border-[rgba(186,215,247,0.12)] text-xs font-mono">
                        <div className="flex items-center gap-3">
                          <span className={`font-bold ${att.passed ? 'text-[#8AA4C4]' : 'text-red-400'}`}>
                            {att.score} / {att.total_questions} ({att.percentage}%)
                          </span>
                          <span className="text-[#526884] text-[11px]">{new Date(att.created_at).toLocaleString()}</span>
                        </div>
                        {att.xp_gained > 0 && <span className="text-[#663af3] font-bold">+{att.xp_gained} XP</span>}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p className="text-[#526884] text-center py-10 font-sans">No quiz questions available for this topic.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default TopicDetail;
