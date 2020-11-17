import { writable } from "svelte/store";

export let Page = writable("index");
export const SnackBars = writable({});
export let Project = writable({});
