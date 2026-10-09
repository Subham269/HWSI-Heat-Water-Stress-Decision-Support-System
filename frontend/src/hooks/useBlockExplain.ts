import useSWR from 'swr';
import { fetchBlockExplanation } from '@/lib/api';

export function useBlockExplain(blockId: string | null, extraDays: number = 0) {
  const { data, error, isLoading } = useSWR(
    blockId ? ['block-explain', blockId, extraDays] : null,
    ([, id, days]) => fetchBlockExplanation(id, days as number),
    { revalidateOnFocus: false }
  );

  return {
    explanation: data,
    error,
    isLoading
  };
}
