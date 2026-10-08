import useSWR from 'swr';
import { fetchRiskIndex } from '@/lib/api';

export function useRiskData(extraDays: number = 0) {
  const { data, error, isLoading, mutate } = useSWR(
    ['risk-index', extraDays],
    ([, days]) => fetchRiskIndex(days as number),
    { revalidateOnFocus: false }
  );

  return {
    data,
    error,
    isLoading,
    mutate
  };
}
