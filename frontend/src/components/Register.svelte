<script>
    import { Page } from "../stores.js";
    import { addSnackbar } from "../utils.js";

    let name, url, email, nick, password, password_repeat, message;
    
    function submit() {
        if (password !== password_repeat) {
            alert("Passwords don't match!")
        } else {
            fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    url: url,
                    email: email,
                    nick: nick,
                    password: password,
                    message: message
                })
            })
            .then(response => response.json())
            .then(data => {
                addSnackbar("FOSSHOST", data["message"], data["success"] ? "green" : "red", 10000)
                if (data["success"]) {
                    setTimeout(function() {
                        $Page = "login"
                    }, 10000)
                }
            })
            .catch(error => alert("Server error: " + error))
        }
    }
</script>

<main>
    <div class="col-md-2">
        <div class="card">
            <div class="card-body danger">
                <img src="/static/assets/img/logo-dark.png"/>
                <hr>
                <div class="form">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Project Name</label>
                                <input class="form-control red-banner" type="text" bind:value={name}>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Project URL (Repo, website, etc.)</label>
                                <input class="form-control red-banner" type="text" bind:value={url}>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Email</label>
                                <input class="form-control red-banner" type="email" bind:value={email}>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Nick (IRC/Matrix/etc.)</label>
                                <input class="form-control red-banner" bind:value={nick}>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Password</label>
                                <input class="form-control red-banner" type="password" bind:value={password}>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Password (repeat)</label>
                                <input class="form-control red-banner" type="password" bind:value={password_repeat}>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Message (tell us a little about your project, or another interesting fact to prove you're not a robot!)</label>
                                <textarea class="form-control red-banner" rows="3" bind:value={message}></textarea>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div class="centered-container">
                        <p>Already have an account? <span on:click={() => $Page = "login"}>Log in</span></p>
                        <button class="btn btn-primary pull-right red-button" on:click={() => submit()}>Register</button>
                    </div>
                    <div class="clearfix"></div>
                </div>
            </div>
        </div>
    </div>
</main>

<style>
    main {
        height: 100%;
        overflow-y: hidden;
    }

    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 75%;
    }

    .red-banner {
        background-image: linear-gradient(to top, #e53935 2px, rgba(156, 39, 176, 0) 2px), linear-gradient(to top, #d2d2d2 1px, rgba(210, 210, 210, 0) 1px);
    }

    .red-button:hover {
        box-shadow: 0 14px 26px -12px #e53935, 0 4px 23px 0px rgba(0, 0, 0, 0.12), 0 8px 10px -5px #ff5350;
        border-color: #ff5350;
        background-color: #ff5350;
    }

    .col-md-2 {
        min-width: 500px;
        height: 100%;
        padding-left: 2px;
        padding-right: 2px;
    }

    .card {
        height: 100%;
        margin-top: 0;
        margin-left: 0;
    }

    .card-body {
        display: flex;
        justify-content: center;
        flex-direction: column;
    }

    .form {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .row {
        width: 80%;
        margin: auto;
    }
</style>
