import React, { useEffect, useState } from 'react';
import { leaderboardService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Trophy, Award, Flame, Zap, Crown, User } from 'lucide-react';

export const Leaderboard = () => {
  const { user } = useAuth();
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const res = await leaderboardService.getLeaderboard();
        setLeaderboard(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchLeaderboard();
  }, []);

  const top3 = leaderboard.slice(0, 3);

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-10 animate-pq-fade-up relative">
      {/* Background Hero Halo */}
      <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[500px] h-[300px] bg-[#663af3]/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="text-center space-y-3 relative z-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[rgba(102,58,243,0.15)] border border-[#663af3]/30 text-[#663af3] text-xs font-mono tracking-widest uppercase backdrop-blur-md">
          <Trophy className="w-3.5 h-3.5" /> GLOBAL LEADERBOARD
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight font-heading authkit-skywash-text">
          Bootcamp Hall of Fame
        </h1>
        <p className="text-[#8AA4C4] text-sm max-w-xl mx-auto leading-relaxed font-sans">
          Compete with fellow bootcamp students, gain XP, and climb the leaderboard ranks!
        </p>
      </div>

      {/* Top 3 Podium */}
      {top3.length > 0 && (
        <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto pt-6 items-end relative z-10">
          {/* #2 Silver */}
          {top3[1] && (
            <div className="authkit-glass-card rounded-[16px] p-5 text-center space-y-2 order-1 shadow-lg border border-[rgba(186,215,247,0.12)] bg-[rgba(186,214,247,0.03)] backdrop-blur-xl">
              <div className="w-10 h-10 rounded-full bg-slate-300 text-slate-950 font-black text-sm flex items-center justify-center mx-auto shadow-md">
                2
              </div>
              <h3 className="font-bold text-[#F0F6FF] text-sm truncate">{top3[1].username}</h3>
              <p className="text-xs font-extrabold text-[#C8DCF5]">{top3[1].xp} XP</p>
              <span className="text-[11px] font-mono text-[#8AA4C4] block">Lvl {top3[1].level}</span>
            </div>
          )}

          {/* #1 Gold */}
          {top3[0] && (
            <div className="authkit-glass-card rounded-[16px] p-6 text-center space-y-2 order-2 border border-[#663af3]/50 bg-[rgba(102,58,243,0.08)] backdrop-blur-xl shadow-[0_0_35px_rgba(102,58,243,0.3)] relative -translate-y-4">
              <div className="absolute -top-6 left-1/2 -translate-x-1/2">
                <Crown className="w-8 h-8 text-amber-400 fill-amber-400 animate-pulse" />
              </div>
              <div className="w-12 h-12 rounded-full bg-amber-400 text-slate-950 font-black text-base flex items-center justify-center mx-auto shadow-lg">
                1
              </div>
              <h3 className="font-extrabold text-[#F0F6FF] text-base truncate font-heading">{top3[0].username}</h3>
              <p className="text-sm font-black text-amber-300">{top3[0].xp} XP</p>
              <span className="text-xs font-mono text-[#8AA4C4] block">Lvl {top3[0].level}</span>
            </div>
          )}

          {/* #3 Bronze */}
          {top3[2] && (
            <div className="authkit-glass-card rounded-[16px] p-5 text-center space-y-2 order-3 shadow-lg border border-[rgba(186,215,247,0.12)] bg-[rgba(186,214,247,0.03)] backdrop-blur-xl">
              <div className="w-10 h-10 rounded-full bg-amber-700 text-white font-black text-sm flex items-center justify-center mx-auto shadow-md">
                3
              </div>
              <h3 className="font-bold text-[#F0F6FF] text-sm truncate">{top3[2].username}</h3>
              <p className="text-xs font-extrabold text-[#C8DCF5]">{top3[2].xp} XP</p>
              <span className="text-[11px] font-mono text-[#8AA4C4] block">Lvl {top3[2].level}</span>
            </div>
          )}
        </div>
      )}

      {/* Rankings List Table */}
      <div className="authkit-glass-card rounded-[16px] p-6 sm:p-8 space-y-4 border border-[rgba(186,215,247,0.12)] bg-[rgba(186,214,247,0.03)] backdrop-blur-xl relative z-10">
        <h3 className="text-lg font-bold font-heading text-[#F0F6FF] mb-4 tracking-tight">
          All Student Rankings
        </h3>

        <div className="space-y-2.5">
          {leaderboard.map((lb) => {
            const isMe = lb.user_id === user?.id;
            return (
              <div
                key={lb.user_id}
                className={`flex items-center justify-between p-4 rounded-[6px] border transition-all ${
                  isMe
                    ? 'bg-[#663af3]/20 border-[#663af3] text-[#F0F6FF] font-bold shadow-[0_0_20px_rgba(102,58,243,0.3)]'
                    : 'bg-[#080917]/80 border-[rgba(186,215,247,0.12)] text-[#C8DCF5] hover:border-[rgba(186,215,247,0.25)]'
                }`}
              >
                <div className="flex items-center gap-4">
                  <span
                    className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs ${
                      lb.rank === 1
                        ? 'bg-amber-400 text-slate-950'
                        : lb.rank === 2
                        ? 'bg-slate-300 text-slate-950'
                        : lb.rank === 3
                        ? 'bg-amber-700 text-white'
                        : 'bg-[rgba(186,215,247,0.08)] text-[#8AA4C4]'
                    }`}
                  >
                    {lb.rank}
                  </span>
                  <div>
                    <h4 className="font-bold text-sm text-[#F0F6FF] flex items-center gap-2">
                      {lb.username} {isMe && <span className="text-[9px] bg-[#663af3] text-white px-2 py-0.5 rounded-full font-mono font-bold tracking-wider">YOU</span>}
                    </h4>
                    <span className="text-xs text-[#8AA4C4] font-mono">Level {lb.level}</span>
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-1.5 text-amber-400 text-xs font-mono">
                    <Flame className="w-4 h-4 fill-amber-400" />
                    <span>{lb.streak}d</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-[#C8DCF5] font-extrabold text-sm min-w-[80px] justify-end font-mono">
                    <Zap className="w-4 h-4 text-[#663af3]" />
                    <span>{lb.xp} XP</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;

