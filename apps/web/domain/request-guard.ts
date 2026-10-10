/**
 * Guards one logical "latest request wins" flow (for example generation).
 * `begin()` aborts any request still in flight and returns a handle whose
 * `isCurrent()` is false once a newer request starts or `cancel()` is called,
 * so a late response or error can never touch a different brand or commerce.
 */
export type RequestHandle = {
  signal: AbortSignal;
  isCurrent: () => boolean;
};

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
