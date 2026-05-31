import React, { useState } from 'react';
import { Icons } from '../../components/ui/Icons';
import { Button } from '../../components/ui/Button';
import { useGeolocation } from '../../hooks/useGeolocation';

interface LocationButtonProps {
  onLocationSelected: (coords: { lat: number; lng: number }) => void;
}

export const LocationButton: React.FC<LocationButtonProps> = ({ onLocationSelected }) => {
  const { getPosition, loading } = useGeolocation();
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [feedback, setFeedback] = useState('');

  const handleClick = async () => {
    setStatus('idle');
    try {
      const coords = await getPosition();
      onLocationSelected(coords);
      setStatus('success');
      setFeedback('Coordinates matched');
      setTimeout(() => { setStatus('idle'); setFeedback(''); }, 3000);
    } catch (err: any) {
      setStatus('error');
      setFeedback(typeof err === 'string' ? err : 'Permission denied');
      setTimeout(() => { setStatus('idle'); setFeedback(''); }, 3000);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <Button
        variant="outline"
        onClick={handleClick}
        disabled={loading}
        className={`h-8 py-1 px-3 text-[11px] font-semibold tracking-tight shrink-0 flex items-center gap-1.5 rounded-md border shadow-xs transition-colors ${
          status === 'success'
            ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
            : status === 'error'
            ? 'border-zinc-200 bg-zinc-50 text-zinc-700'
            : 'bg-white border-zinc-200 hover:bg-zinc-50 text-zinc-600'
        }`}
      >
        <Icons.MapPin size={12} className={loading ? 'animate-pulse text-zinc-400' : 'text-zinc-500'} />
        {loading ? 'Reading Coordinates...' : status === 'success' ? 'Coordinates Synced' : 'Share Location'}
      </Button>
      {feedback && (
        <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400">
          {feedback}
        </span>
      )}
    </div>
  );
};