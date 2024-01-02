import { writable } from 'svelte/store';

function createFunctionTrigger() {
  const { subscribe, set } = writable(null);

  return {
    subscribe,
    broadcast: (data) => set(data),
  };
}

export const splashPromptTrigger = createFunctionTrigger();
export const loadingTextTrigger = createFunctionTrigger();
export const currentPageTrigger = createFunctionTrigger();
export const courseObjectTrigger = createFunctionTrigger();