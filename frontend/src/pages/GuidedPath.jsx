import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { topicService } from '../services/api';
import { CheckCircle2, Circle, ArrowRight, ShieldCheck, Map } from 'lucide-react';

export const GuidedPath = () => {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const res = await topicService.getTopics();
        setTopics(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchTopics();
  }, []);

  // Group by Levels
  const levelsMap = topics.reduce((acc, topic) => {
    const lvlKey = topic.level_title || `Level ${topic.level_number}`;
    if (!acc[lvlKey]) acc[lvlKey] = [];
    acc[lvlKey].push(topic);
    return acc;
  }, {});

  return (
    <div className="max-w-[1000px] mx-auto px-4 py-12 space-y-14 animate-pq-fade-up">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[rgba(186,214,247,0.04)] border border-[rgba(186,215,247,0.14)] text-[#C8DCF5] text-xs font-mono">
          <ShieldCheck className="w-3.5 h-3.5 text-[#663af3]" /> RECOMMENDED CURRICULUM ARCHITECTURE
        </div>
        <h1 className="text-4xl sm:text-6xl font-heading font-medium authkit-heading-gradient tracking-tight">
          Python Engineering Roadmap
        </h1>
        <p className="text-[#8AA4C4] text-sm max-w-xl mx-auto leading-relaxed font-sans">
          Follow our recommended step-by-step curriculum or jump freely between modules anytime.
        </p>
      </div>

      {/* Path Roadmap Node Tree with Luminous Line */}
      <div className="space-y-16 relative before:absolute before:inset-0 before:left-1/2 before:-translate-x-1/2 before:w-[2px] before:bg-gradient-to-b before:from-[#663af3] before:via-[rgba(186,215,247,0.3)] before:to-transparent">
        {Object.entries(levelsMap).map(([levelTitle, levelTopics]) => (
          <div key={levelTitle} className="space-y-8 relative z-10">
            {/* Level Banner */}
            <div className="flex justify-center">
              <span className="bg-[#05060f] border border-[rgba(186,215,247,0.18)] text-[#F0F6FF] px-6 py-2 rounded-full font-eyebrow text-xs uppercase tracking-widest shadow-glass-elevation">
                {levelTitle}
              </span>
            </div>

            {/* Nodes in this level */}
            <div className="space-y-8">
              {levelTopics.map((topic, idx) => {
                const isCompleted = topic.is_completed;
                const isEven = idx % 2 === 0;

                return (
                  <div
                    key={topic.id}
                    className={`flex flex-col sm:flex-row items-center gap-6 ${
                      isEven ? 'sm:flex-row-reverse' : ''
                    }`}
                  >
                    {/* Topic Card */}
                    <div className="w-full sm:w-1/2">
                      <div
                        className={`authkit-glass-card p-6 rounded-card ${
                          isCompleted ? 'border-[#663af3]/40 bg-[rgba(102,58,243,0.06)]' : ''
                        }`}
                      >
                        <div className="flex items-center justify-between mb-3">
                          <span className="font-mono text-[11px] uppercase tracking-wider text-[#526884]">
                            Module #{topic.order_index}
                          </span>
                          {isCompleted ? (
                            <span className="flex items-center gap-1 text-xs font-medium text-[#F0F6FF] bg-[rgba(186,214,247,0.08)] px-3 py-0.5 rounded-full border border-[rgba(186,215,247,0.2)]">
                              <CheckCircle2 className="w-3.5 h-3.5 text-[#663af3]" /> Completed
                            </span>
                          ) : (
                            <span className="text-xs text-[#8AA4C4] font-medium bg-[rgba(186,214,247,0.04)] px-3 py-0.5 rounded-full border border-[rgba(186,215,247,0.12)]">Available</span>
                          )}
                        </div>

                        <h3 className="text-xl font-heading font-semibold text-[#F0F6FF] mb-2">{topic.title}</h3>
                        <p className="text-[#8AA4C4] text-xs line-clamp-2 mb-5 leading-relaxed font-sans">{topic.description}</p>

                        <Link
                          to={`/topic/${topic.id}`}
                          className={`inline-flex items-center gap-2 px-5 py-2 rounded-md text-xs font-semibold transition-all ${
                            isCompleted
                              ? 'authkit-btn-ghost'
                              : 'authkit-btn-violet shadow-[0_0_15px_rgba(102,58,243,0.4)]'
                          }`}
                        >
                          {isCompleted ? 'Review Module' : 'Start Module'} <ArrowRight className="w-3.5 h-3.5" />
                        </Link>
                      </div>
                    </div>

                    {/* Central Connected Node Circle */}
                    <div className="hidden sm:flex w-10 h-10 rounded-full bg-[#05060f] border-2 border-[#663af3] items-center justify-center shadow-[0_0_20px_rgba(102,58,243,0.4)] z-10 shrink-0">
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5 text-[#F0F6FF]" />
                      ) : (
                        <Circle className="w-4 h-4 text-[#663af3] fill-[#663af3]/30" />
                      )}
                    </div>

                    {/* Empty balancing side */}
                    <div className="hidden sm:block w-1/2" />
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GuidedPath;
