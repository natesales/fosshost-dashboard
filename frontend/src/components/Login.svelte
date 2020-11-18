<script>
    import {Page} from "../stores.js";
    import {addSnackbar, checkLogin} from "../utils.js";

    let email, password;

    function submit() {
        fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    checkLogin($Page)
                    $Page = "dashboard"
                } else {
                    addSnackbar("Error", data["message"], data["success"] ? "green" : "red")
                }
            })
            .catch(error => alert("Server error: " + error))
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
                                <label class="bmd-label-floating">Email</label>
                                <input bind:value={email} class="form-control red-banner" type="email">
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-floating">Password</label>
                                <input bind:value={password} class="form-control red-banner" type="password">
                            </div>
                        </div>
                    </div>
                    <br>
                    <div class="centered-container">
                        <p>Don't have an account? <span on:click={() => $Page = "register"}>Register</span></p>
                        <button class="btn btn-primary pull-right red-button" on:click={() => submit()}>Login</button>
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
