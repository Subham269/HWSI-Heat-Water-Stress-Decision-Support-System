import { useState } from 'react';
import { postAllocation } from '@/lib/api';
import type { AllocationResponse } from '@/lib/types';

export function useAllocation() {
  const [result, setResult] = useState<AllocationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const allocate = async (tankers: number, coolingUnits: number, extraDays?: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await postAllocation({ tankers, cooling_units: coolingUnits, extra_days: extraDays });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Allocation failed'));
    } finally {
      setIsLoading(false);
    }
  };

  return { allocate, result, isLoading, error };
}
