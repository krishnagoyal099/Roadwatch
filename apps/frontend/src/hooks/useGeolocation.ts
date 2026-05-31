import { useState } from 'react';

export interface Coords {
  lat: number;
  lng: number;
}

export function useGeolocation() {
  const [loading, setLoading] = useState(false);
  const [coords, setCoords] = useState<Coords | null>(null);
  const [error, setError] = useState<string | null>(null);

  const getPosition = (): Promise<Coords> => {
    setLoading(true);
    setError(null);
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        const msg = 'Geolocation is not supported by your browser.';
        setError(msg);
        setLoading(false);
        reject(msg);
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const matched = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          setCoords(matched);
          setLoading(false);
          resolve(matched);
        },
        (err) => {
          let msg = 'Failed to retrieve location.';
          if (err.code === 1) msg = 'Location access denied.';
          setError(msg);
          setLoading(false);
          reject(msg);
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    });
  };

  return { getPosition, coords, loading, error };
}