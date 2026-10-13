/** Prevent stale async work from updating a newly selected brand or commerce. */
export type RequestHandle = { signal: AbortSignal; isCurrent: () => boolean };

export function createRequestGuard() {
  let sequence = 0;
  let controller: AbortController | null = null;

  function cancel() {
    sequence += 1;
    controller?.abort();
    controller = null;
  }

  function begin(): RequestHandle {
    cancel();
    const mine = sequence;
    const own = new AbortController();
    controller = own;
    return { signal: own.signal, isCurrent: () => mine === sequence && !own.signal.aborted };
  }

  return { begin, cancel };
}
