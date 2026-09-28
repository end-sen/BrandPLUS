import React from 'react';
import { AlertTriangle, Bell, Info, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function AlertsPanel({ alerts, onMarkAlertRead }) {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-center items-center text-slate-400 text-xs">
        <CheckCircle2 className="w-8 h-8 text-emerald-500 mb-2" />
        <span className="font-semibold text-emerald-400">All systems nominal</span>
        <span className="text-[11px] text-slate-500 mt-0.5">No critical anomalies or negative spikes detected.</span>
      </div>
    );
  }

  const getAlertStyle = (severity) => {
    switch (severity) {
      case 'critical':
        return {
          bg: 'bg-rose-950/30 border-rose-500/30 text-rose-300',
          icon: ShieldAlert,
          iconColor: 'text-rose-400',
          badge: 'bg-rose-500/20 text-rose-300 border-rose-500/40',
        };
      case 'warning':
        return {
          bg: 'bg-amber-950/30 border-amber-500/30 text-amber-300',
          icon: AlertTriangle,
          iconColor: 'text-amber-400',
          badge: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
        };
      default:
        return {
          bg: 'bg-indigo-950/30 border-indigo-500/30 text-indigo-300',
          icon: Info,
          iconColor: 'text-indigo-400',
          badge: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40',
        };
    }
  };

  const unreadCount = alerts.filter((a) => !a.is_read).length;

  return (
    <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-between glass-card-hover">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <Bell className="w-4 h-4 text-amber-400 animate-pulse-slow" />
          <h3 className="font-bold text-sm text-white">Anomalies & Reputation Alerts</h3>
        </div>
        {unreadCount > 0 && (
          <span className="px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/40 text-rose-400 text-[10px] font-bold">
            {unreadCount} Unread
          </span>
        )}
      </div>

      <div className="space-y-2.5 overflow-y-auto max-h-60 pr-1">
        {alerts.map((a) => {
          const style = getAlertStyle(a.severity);
          const Icon = style.icon;

          return (
            <div
              key={a.id}
              className={`p-3 rounded-xl border transition-all text-xs ${style.bg} ${
                a.is_read ? 'opacity-60' : 'opacity-100 shadow-md'
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-start space-x-2.5">
                  <Icon className={`w-4 h-4 shrink-0 mt-0.5 ${style.iconColor}`} />
                  <div>
                    <div className="flex items-center space-x-2">
                      <h4 className="font-bold text-white text-xs">{a.title}</h4>
                      <span className={`px-1.5 py-0.2 rounded text-[9px] font-extrabold uppercase border ${style.badge}`}>
                        {a.severity}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-300 mt-1 leading-relaxed">{a.message}</p>
                    <span className="text-[10px] text-slate-400 mt-1 block">
                      {new Date(a.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>

                {!a.is_read && (
                  <button
                    onClick={() => onMarkAlertRead(a.id)}
                    className="text-[10px] font-semibold text-slate-400 hover:text-white bg-slate-900 border border-slate-700 px-2 py-1 rounded-lg shrink-0 transition-colors"
                  >
                    Dismiss
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
