import useSWR from 'swr';
import { fetchBlockExplanation } from '@/lib/api';

export function useBlockExplain(blockId: string | null) {
  const { data, error, isLoading } = useSWR(
    blockId ? ['block-explain', blockId] : null,
    ([, id]) => fetchBlockExplanation(id),
    { revalidateOnFocus: false }
  );

  return {
    explanation: data,
    error,
    isLoading
  };
}
