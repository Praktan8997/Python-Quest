import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { topicService } from '../services/api';
import { Flame, Zap, CheckCircle2, ArrowRight, Play, Code, Layers, GitBranch, Settings, Compass, History, Sparkles, ShieldCheck, Trophy } from 'lucide-react';

export const Dashboard = () => {
  const { user, progressSummary } = useAuth();
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const topRes = await topicService.getTopics();
        setTopics(topRes.data);
      } catch (err) {
        console.error('Failed to load dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    loadDashboardData();
  }, []);

  const nextTopic = topics.find(t => !t.is_completed) || topics[0];

  const categories = [
    {
      title: "Basics",
      icon: Code,
      topics: topics.filter(t => t.level_title === "Basics")
    },
    {
      title: "Collections",
      icon: Layers,
      topics: topics.filter(t => t.level_title === "Collections")
    },
    {
      title: "Control Flow",
      icon: GitBranch,
      topics: topics.filter(t => t.level_title === "Control flow")
    },
    {
      title: "Functions & Tools",
      icon: Settings,
      topics: topics.filter(t => t.level_title === "Functions & tools")
    }
  ];

  return (
    <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16 animate-pq-fade-up">
      {/* HERO BANNER - Cathedral Launchpad Atmosphere */}
      <div className="relative overflow-hidden rounded-card authkit-glass-card p-8 sm:p-12 shadow-glass-elevation border border-[rgba(186,215,247,0.12)]">
        {/* Spotlight Glow Effect behind Hero */}
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-[#663af3]/15 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-10">
          <div className="space-y-6 max-w-2xl">
            {/* Eyebrow Label with Hairline Line */}
            <div className="flex items-center gap-3">
              <span className="h-[1px] w-8 bg-gradient-to-r from-transparent to-[#8AA4C4]" />
              <span className="font-eyebrow text-[11px] text-[#8AA4C4] uppercase tracking-[0.12em] flex items-center gap-2">
                <ShieldCheck className="w-3.5 h-3.5 text-[#663af3]" /> WELCOME BACK, {user?.full_name || user?.username || 'DEVELOPER'}
              </span>
            </div>

            <h1 className="text-4xl sm:text-6xl font-heading font-medium authkit-heading-gradient leading-[1.12] tracking-tight">
              Master Python Syntax in Midnight Cathedral.
            </h1>

            <p className="text-[#C8DCF5]/80 text-base sm:text-lg leading-relaxed font-sans">
              Execute isolated Python code challenges, pass comprehensive quizzes, and elevate your bootcamp engineering rank.
            </p>

            {/* Level Progression */}
            {progressSummary && (
              <div className="pt-2 max-w-lg space-y-2.5">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="text-[#8AA4C4]">Level {user?.level || 1} Progression</span>
                  <span className="text-[#F0F6FF] font-bold">
                    {progressSummary.xp_level_percentage}% ({progressSummary.xp_to_next_level} XP needed)
                  </span>
                </div>
                <div className="w-full bg-[rgba(186,214,247,0.06)] rounded-full h-2.5 overflow-hidden border border-[rgba(186,215,247,0.12)] p-0.5">
                  <div
                    className="bg-[#663af3] h-full rounded-full transition-all duration-1000 shadow-[0_0_12px_#663af3]"
                    style={{ width: `${progressSummary.xp_level_percentage}%` }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* User Live Stats Glass Plate */}
          <div className="flex items-center gap-4 bg-[rgba(186,214,247,0.04)] border border-[rgba(186,215,247,0.14)] p-6 rounded-card shadow-glass-elevation shrink-0">
            <div className="text-center px-4 border-r border-[rgba(186,215,247,0.12)]">
              <span className="block text-3xl font-heading font-bold text-[#F0F6FF]">{user?.level || 1}</span>
              <span className="font-eyebrow text-[9px] text-[#526884] uppercase tracking-widest mt-1 block">LEVEL</span>
            </div>
            <div className="text-center px-4 border-r border-[rgba(186,215,247,0.12)]">
              <span className="block text-3xl font-heading font-bold text-[#C8DCF5]">{user?.xp || 0}</span>
              <span className="font-eyebrow text-[9px] text-[#526884] uppercase tracking-widest mt-1 block">TOTAL XP</span>
            </div>
            <div className="text-center px-4">
              <span className="block text-3xl font-heading font-bold text-[#F0F6FF] flex items-center justify-center gap-1">
                <Flame className="w-6 h-6 text-[#663af3] fill-[#663af3]" /> {user?.current_streak || 1}
              </span>
              <span className="font-eyebrow text-[9px] text-[#526884] uppercase tracking-widest mt-1 block">STREAK</span>
            </div>
          </div>
        </div>
      </div>

      {/* CURRICULUM MODULES - Cathedral Grid */}
      <div className="space-y-8">
        <div className="flex items-center justify-between border-b border-[rgba(186,215,247,0.12)] pb-4">
          <div className="flex items-center gap-3">
            <span className="h-4 w-1 bg-[#663af3] rounded-full" />
            <h2 className="text-2xl font-heading font-medium text-[#F0F6FF] tracking-tight">
              Curriculum Modules
            </h2>
          </div>
          <Link to="/explore" className="font-eyebrow text-xs text-[#8AA4C4] hover:text-[#F0F6FF] uppercase tracking-widest transition-colors">
            VIEW ALL MODULES →
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((cat) => {
            const IconComp = cat.icon;
            const completedCount = cat.topics.filter(t => t.is_completed).length;

            return (
              <div
                key={cat.title}
                className="authkit-glass-card p-6 flex flex-col justify-between space-y-6 rounded-card"
              >
                <div className="space-y-5">
                  <div className="flex items-center gap-3.5">
                    {/* Circular Frosted Icon Tile (9999px circle) */}
                    <div className="w-11 h-11 rounded-circle bg-[rgba(186,214,247,0.06)] border border-[rgba(186,215,247,0.14)] flex items-center justify-center shrink-0 text-[#F0F6FF]">
                      <IconComp className="w-5 h-5 text-[#C8DCF5]" />
                    </div>
                    <h3 className="text-base font-heading font-semibold text-[#F0F6FF] leading-tight">
                      {cat.title}
                    </h3>
                  </div>

                  <ul className="space-y-2 pt-1">
                    {cat.topics.map((t) => (
                      <li key={t.id}>
                        <Link
                          to={`/topic/${t.id}`}
                          className="flex items-center justify-between p-2.5 rounded-md hover:bg-[rgba(186,214,247,0.06)] transition-colors group/item"
                        >
                          <span className="text-xs font-medium text-[#8AA4C4] group-hover/item:text-[#F0F6FF] flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#526884] group-hover/item:bg-[#663af3]" />
                            {t.title}
                          </span>
                          {t.is_completed ? (
                            <CheckCircle2 className="w-4 h-4 text-[#8AA4C4] shrink-0" />
                          ) : (
                            <ArrowRight className="w-3.5 h-3.5 text-[#526884] group-hover/item:text-[#F0F6FF] shrink-0 opacity-0 group-hover/item:opacity-100 transition-all" />
                          )}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="pt-4 border-t border-[rgba(186,215,247,0.12)] flex items-center justify-between text-xs text-[#526884] font-mono">
                  <span>{completedCount}/{cat.topics.length} Mastered</span>
                  <Link to="/explore" className="text-[#8AA4C4] hover:text-[#F0F6FF] font-sans font-medium flex items-center gap-1">
                    Open →
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* LOWER SECTION - Continue & Recent Activity */}
      <div className="space-y-8 pt-4">
        {nextTopic && (
          <div className="authkit-glass-card p-8 relative overflow-hidden rounded-card">
            <div className="flex items-center justify-between mb-4">
              <span className="font-eyebrow text-[10px] text-[#F0F6FF] flex items-center gap-2 bg-[rgba(186,214,247,0.06)] px-3.5 py-1 rounded-badge border border-[rgba(186,215,247,0.14)]">
                <Play className="w-3 h-3 text-[#663af3] fill-[#663af3]" /> CONTINUE LEARNING
              </span>
              <span className="text-xs text-[#526884] font-mono">{nextTopic.level_title}</span>
            </div>

            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
              <div className="space-y-1">
                <h3 className="text-2xl font-heading font-semibold text-[#F0F6FF]">
                  {nextTopic.title}
                </h3>
                <p className="text-[#8AA4C4] text-sm">{nextTopic.description}</p>
              </div>
              <Link
                to={`/topic/${nextTopic.id}`}
                className="authkit-btn-violet px-6 py-2.5 text-xs rounded-md font-semibold flex items-center gap-2 shrink-0 shadow-[0_0_20px_rgba(102,58,243,0.4)]"
              >
                Resume Quest <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        )}

        {/* Recent Submissions */}
        {progressSummary?.recent_submissions?.length > 0 && (
          <div className="authkit-glass-card p-8 space-y-5 rounded-card">
            <h3 className="text-lg font-heading font-semibold text-[#F0F6FF] flex items-center gap-2.5">
              <History className="w-5 h-5 text-[#8AA4C4]" /> Recent Submissions
            </h3>
            <div className="space-y-3">
              {progressSummary.recent_submissions.map((sub) => (
                <div key={sub.id} className="flex items-center justify-between p-4 rounded-md bg-[rgba(186,214,247,0.02)] border border-[rgba(186,215,247,0.12)] text-xs">
                  <div className="flex items-center gap-3">
                    {sub.passed ? (
                      <span className="w-6 h-6 rounded-full bg-[rgba(186,214,247,0.1)] text-[#F0F6FF] border border-[rgba(186,215,247,0.2)] flex items-center justify-center font-bold">✓</span>
                    ) : (
                      <span className="w-6 h-6 rounded-full bg-red-500/10 text-red-400 border border-red-500/30 flex items-center justify-center font-bold">✕</span>
                    )}
                    <div>
                      <span className="font-medium text-[#F0F6FF] block">Challenge #{sub.challenge_id}</span>
                      <span className="text-[11px] text-[#526884] font-mono">{new Date(sub.created_at).toLocaleString()}</span>
                    </div>
                  </div>
                  <span className={`font-mono font-bold ${sub.passed ? 'text-[#8AA4C4]' : 'text-red-400'}`}>
                    {sub.passed ? 'Passed' : 'Failed'} ({sub.execution_time_ms}ms)
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
