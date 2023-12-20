import { writable } from 'svelte/store';

function createFunctionTrigger() {
  const { subscribe, set } = writable(null);

  return {
    subscribe,
    broadcast: (data) => set(data),
  };
}

export const splashPromptTrigger = createFunctionTrigger();