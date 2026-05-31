import React, { useState } from 'react';
import { MapPin, Check, AlertCircle } from 'lucide-react';
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
      setFeedback('Location matched!');
      setTimeout(() => { setStatus('idle'); setFeedback(''); }, 3500);
    } catch (err: any) {
      setStatus('error');
      setFeedback(typeof err === 'string' ? err : 'Permission denied.');
      setTimeout(() => { setStatus('idle'); setFeedback(''); }, 4000);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <Button
        variant="outline"
        onClick={handleClick}
        disabled={loading}
        className={`h-9 py-1 px-3.5 text-xs font-semibold shrink-0 flex items-center gap-1.5 rounded-full border border-slate-200 shadow-xs transition-colors ${
          status === 'success'
            ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
            : status === 'error'
            ? 'border-rose-200 bg-rose-50 text-rose-700'
            : 'bg-white hover:bg-slate-50 text-slate-600'
        }`}
      >
        {status === 'success' ? (
          <Check className="w-3.5 h-3.5 text-emerald-600" />
        ) : (
          <MapPin className={`w-3.5 h-3.5 ${loading ? 'animate-pulse text-blue-500' : 'text-slate-500'}`} />
        )}
        {loading ? 'Retrieving coordinates...' : status === 'success' ? 'Location verified' : 'Share My Location'}
      </Button>
      {feedback && (
        <span className={`text-[11px] font-medium flex items-center gap-1 ${
          status === 'error' ? 'text-rose-600' : 'text-emerald-600'
        }`}>
          {status === 'error' && <AlertCircle className="w-3 h-3 shrink-0" />}
          {feedback}
        </span>
      )}
    </div>
  );
};