<script>
    import {addSnackbar, checkLogin} from "../utils";
    import Spinner from "./Spinner.svelte";
    import {Page, Project} from "../stores.js";

    let password, password_repeat, key = "";

    function submitPasswordChange() {
        if (password !== password_repeat) {
            alert("Passwords don't match!")
        } else {
            fetch("/api/auth/change", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    password: password
                }),
                credentials: "include"
            })
                .then(response => response.json())
                .then(data => addSnackbar("Profile", data["message"], data["success"] ? "green" : "red"))
                .catch(error => alert("Server error: " + error))
        }
    }

    function addKey() {
        fetch("/api/auth/add_key", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                key: key
            }),
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                key = ""
                addSnackbar("SSH Keys", data["message"], data["success"] ? "green" : "red")
                if (data["success"]) {
                    fetch("/api/auth/check", {
                        credentials: "include"
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data["success"]) {
                                Project.set(data["message"])
                            }
                        })
                }
            })
            .catch(error => alert("Server error: " + error))
    }
</script>

<main>
    <div class="col-md-7">
        <div class="card">
            <div class="card-header card-header-danger">
                <h4 class="card-title">Profile Settings</h4>
                <p class="card-category">Modify your account and project settings</p>
            </div>
            <div class="card-body danger">
                <div>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Password</label>
                                <input bind:value={password} class="form-control red-banner" type="password">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Password (repeat)</label>
                                <input bind:value={password_repeat} class="form-control red-banner" type="password">
                            </div>
                        </div>
                    </div>
                    <button class="btn btn-primary pull-right red-button" on:click={() => submitPasswordChange()} type="submit">Submit</button>
                    <div class="clearfix"></div>
                </div>
            </div>
        </div>
    </div>

    <br>

    <div class="col-md-7">
        <div class="card">
            <div class="card-header card-header-danger">
                <h4 class="card-title">SSH Keys</h4>
                <p class="card-category">Manage your SSH keys</p>
            </div>
            <div class="card-body danger">
                <div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">SSH Key (ssh-ed25519...)</label>
                                <input bind:value={key} class="form-control red-banner" type="text">
                            </div>
                        </div>
                    </div>
                    <button class="btn btn-primary pull-right red-button" on:click={() => addKey()} type="submit">Add</button>
                    {#if $Project["ssh-keys"]}
                        {#if $Project["ssh-keys"].length === 0}
                            <p>You don't have any SSH keys configured. Add one to get started!</p>
                        {:else}
                            <p>SSH Keys:</p>
                            <ul class="key-list">
                                {#each $Project["ssh-keys"] as key}
                                    <li>{key}</li>
                                {/each}
                            </ul>
                        {/if}
                    {:else}
                        <p>You don't have any SSH keys configured. Add one to get started!</p>
                    {/if}
                    <div class="clearfix"></div>
                </div>
            </div>
        </div>
    </div>
</main>

<style>
    .red-banner {
        background-image: linear-gradient(to top, #e53935 2px, rgba(156, 39, 176, 0) 2px), linear-gradient(to top, #d2d2d2 1px, rgba(210, 210, 210, 0) 1px);
    }

    .red-button:hover {
        box-shadow: 0 14px 26px -12px #e53935, 0 4px 23px 0 rgba(0, 0, 0, 0.12), 0 8px 10px -5px #ff5350;
        border-color: #ff5350;
        background-color: #ff5350;
    }

    .key-list {
        font-family: 'Consolas', 'Deja Vu Sans Mono', 'Bitstream Vera Sans Mono', monospace;
    }
</style>
