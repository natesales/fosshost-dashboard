import { writable } from "svelte/store";

export let Page = writable("login");
export const SnackBars = writable({});
