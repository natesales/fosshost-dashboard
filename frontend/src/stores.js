import { writable } from "svelte/store";

export let Page = writable("index");
export const SnackBars = writable({});
export let Project = writable({});
export let Counters = writable({
    "vms": 0,
    "keys": 0,
    "locations": 0,
    "alerts": 0,
});
