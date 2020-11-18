<script>
    import StatBoxes from "./StatBoxes.svelte";
    import {Counters, Page} from "../stores.js";
    import {onMount} from "svelte";
    import {addSnackbar} from "../utils.js";

    let vms = [];
    let locations = new Set();

    $: {
        $Counters.vms = vms.length;
        $Counters.locations = locations.size
    }

    function loadVms() {
        fetch("/api/virt/list", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                vms = data["results"]
                for (const vm in vms) {
                    locations.add(vms[vm]["cluster"]["value"])
                }
            })
            .catch(error => alert("Server error: " + error))
    }

    function deprovision(hostname, hypervisor) {
        fetch("/api/virt/deprovision", {
            credentials: "include",
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                hostname: hostname,
                hypervisor: hypervisor
            })
        })
            .then(response => response.json())
            .then(data => {
                addSnackbar("Deprovision", data["message"], data["success"] ? "green" : "red")
            })
            .catch(error => alert("Server error: " + error))
    }

    onMount(() => loadVms())
</script>

<main>
    <StatBoxes/>
    <div class="row">
        <div class="col-lg-12">
            <div class="card">
                <div class="card-header card-header-danger">
                    <h4 class="card-title">
                        Virtual Machines
                    </h4>
                    <p class="card-category">
                        <u><a on:click={() => {$Page = "request"}}>Infrastructure Request</a></u>
                    </p>
                </div>
                <div class="card-body table-responsive">
                    <table class="table table-hover">
                        <thead>
                        <tr>
                            <th>Hostname</th>
                            <th>Status</th>
                            <th>Addresses</th>
                            <th>Resources</th>
                            <th>Hypervisor</th>
                            <th>Control</th>
                        </tr>
                        </thead>
                        <tbody>

                        {#each vms as vm}
                            <tr>
                                <td>{ vm["name"] }</td>
                                <td>
                                    {#if vm["status"]["value"] === "active"}
                                        <i class="material-icons color-green">done</i>
                                    {:else}
                                        {vm["status"]["label"]}
                                    {/if}
                                </td>
                                <td>{vm["primary_ip4"]["address"]}<br/>{vm["primary_ip6"]["address"]}</td>
                                <td>
                                    {vm["vcpus"]} vCPU{vm["vcpus"] > 1 ? "s" : ""} / {vm["memory"] / 1000}GB RAM / { vm["disk"] }GB Disk
                                </td>
                                <td>{vm["cluster"]["name"]}</td>
                                <td>
                                    <input class="control-button button-blue" onclick="alert('This would open the console')" type="button" value="Console"/>
                                    <button class="control-button button-red" on:click={deprovision(vm["name"], vm["cluster"]["name"])}>Deprovision</button>
                                </td>
                            </tr>
                        {/each}

                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</main>

<style>
    .control-button {
        cursor: pointer;
    }
</style>