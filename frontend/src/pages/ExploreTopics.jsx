import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { topicService } from '../services/api';
import { Compass, CheckCircle2, ArrowRight, Layers, Search, ShieldCheck } from 'lucide-react';

export const ExploreTopics = () => {
  const [topics, setTopics] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');
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

  const categories = ['All', 'Basics', 'Collections', 'Control flow', 'Functions & tools'];

  const filteredTopics = topics.filter((t) => {
    const matchesSearch = t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          t.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = activeCategory === 'All' || t.level_title === activeCategory;
    return matchesSearch && matchesCategory;
  });

  const levelsMap = filteredTopics.reduce((acc, topic) => {
    const lvlKey = topic.level_title || `Level ${topic.level_number}`;
    if (!acc[lvlKey]) acc[lvlKey] = [];
    acc[lvlKey].push(topic);
    return acc;
  }, {});

  return (
    <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12 animate-pq-fade-up">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-4 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[rgba(186,214,247,0.04)] border border-[rgba(186,215,247,0.14)] text-[#C8DCF5] text-xs font-mono">
            <ShieldCheck className="w-3.5 h-3.5 text-[#663af3]" /> OPEN CURRICULUM ARCHITECTURE
          </div>
          <h1 className="text-4xl sm:text-6xl font-heading font-medium authkit-heading-gradient tracking-tight">
            All Python Topics & Modules
          </h1>
          <p className="text-[#8AA4C4] text-sm leading-relaxed font-sans">
            Explore topics freely based on your interests or bootcamp engineering goals.
          </p>
        </div>

        {/* Search Bar (6px radius) */}
        <div className="relative min-w-[280px]">
          <Search className="w-4 h-4 text-[#8AA4C4] absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search modules..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-11 pr-4 py-2.5 rounded-badge bg-[rgba(186,214,247,0.03)] border border-[rgba(186,215,247,0.14)] text-[#F0F6FF] placeholder-[#526884] text-xs font-medium focus:outline-none focus:border-[#663af3] shadow-inner transition-colors"
          />
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all shrink-0 ${
              activeCategory === cat
                ? 'bg-[rgba(186,214,247,0.08)] text-[#F0F6FF] border border-[rgba(186,215,247,0.24)] shadow-sm'
                : 'bg-[rgba(186,214,247,0.03)] border border-[rgba(186,215,247,0.12)] text-[#8AA4C4] hover:text-[#F0F6FF]'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Topics by Level */}
      <div className="space-y-12">
        {Object.keys(levelsMap).length === 0 ? (
          <div className="authkit-glass-card p-12 text-center text-[#8AA4C4] space-y-3 rounded-card">
            <Search className="w-8 h-8 text-[#8AA4C4] mx-auto" />
            <p className="text-sm font-semibold">No topics matched your search query.</p>
          </div>
        ) : (
          Object.entries(levelsMap).map(([levelTitle, levelTopics]) => (
            <div key={levelTitle} className="space-y-6">
              <h2 className="text-xl font-heading font-medium text-[#F0F6FF] flex items-center gap-2.5 border-b border-[rgba(186,215,247,0.12)] pb-3">
                <Layers className="w-5 h-5 text-[#8AA4C4]" /> {levelTitle}
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {levelTopics.map((topic) => (
                  <Link
                    key={topic.id}
                    to={`/topic/${topic.id}`}
                    className="authkit-glass-card-interactive p-6 flex flex-col justify-between group rounded-card"
                  >
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="w-8 h-8 rounded-full bg-[rgba(186,214,247,0.06)] border border-[rgba(186,215,247,0.12)] flex items-center justify-center text-[#8AA4C4] font-mono font-bold text-xs">
                          #{topic.order_index}
                        </span>
                        {topic.is_completed && (
                          <span className="flex items-center gap-1 text-[11px] font-medium text-[#F0F6FF] bg-[rgba(186,214,247,0.08)] px-2.5 py-0.5 rounded-full border border-[rgba(186,215,247,0.2)]">
                            <CheckCircle2 className="w-3.5 h-3.5 text-[#663af3]" /> Done
                          </span>
                        )}
                      </div>

                      <div>
                        <h3 className="text-lg font-heading font-semibold text-[#F0F6FF] group-hover:text-[#F0F6FF] transition-colors">
                          {topic.title}
                        </h3>
                        <p className="text-[#8AA4C4] text-xs mt-1.5 line-clamp-2 leading-relaxed font-sans">{topic.description}</p>
                      </div>
                    </div>

                    <div className="pt-4 mt-4 border-t border-[rgba(186,215,247,0.12)] flex items-center justify-between text-xs font-mono text-[#526884] group-hover:text-[#8AA4C4] transition-colors">
                      <span>{topic.challenges_count || 1} Challenge</span>
                      <span className="flex items-center gap-1 font-sans text-[#8AA4C4]">Open <ArrowRight className="w-3.5 h-3.5" /></span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ExploreTopics;
