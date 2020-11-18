<script>
    import Sidebar from "./components/Sidebar.svelte";
    import Navbar from "./components/Navbar.svelte";
    import Footer from "./components/Footer.svelte";
    import Profile from "./components/Profile.svelte";
    import {Page, Project} from "./stores.js";
    import RequestForm from "./components/RequestForm.svelte";
    import Dashboard from "./components/Dashboard.svelte";
    import Login from "./components/Login.svelte";
    import Register from "./components/Register.svelte";
    import SnackbarGroup from "./components/SnackbarGroup.svelte";
    import {onMount} from "svelte";
    import Spinner from "./components/Spinner.svelte";
    import {checkLogin, logOut} from "./utils";

    // Set title
    $: {
        document.title = $Page.charAt(0).toUpperCase() + $Page.slice(1) + " | FOSSHOST"
    }

    onMount(() => checkLogin())

    $: checkLogin($Page)

    // Show help message after 4 seconds
    let showHelp = false
    setTimeout(() => {
        if ($Page === "index") {
            showHelp = true
            logOut();
        }
    }, 4000)
</script>

<main>
    {#if $Page === "index"}
        <div class="index-container">
            <img src="/static/assets/img/logo-dark.png" width="15%"/>
            <Spinner/>
            {#if showHelp}
                <p>Having trouble? Check our <a href="https://status.fosshost.org">statuspage</a> or <a href="https://fosshost.org/contact">contact</a> us.</p>
            {/if}
        </div>
    {:else if $Page === "login"}
        <Login/>
    {:else if $Page === "register"}
        <Register/>
    {:else}
        <div class="wrapper">
            <Sidebar/>
            <div class="main-panel">
                <Navbar projectName="delivr"/>
                <div class="content">
                    <div class="container-fluid">
                        {#if $Page === "dashboard"}
                            <Dashboard/>
                        {:else if $Page === "profile"}
                            <Profile/>
                        {:else if $Page === "request"}
                            <RequestForm/>
                        {/if}
                    </div>
                </div>
                <Footer/>
            </div>
        </div>
    {/if}

    <SnackbarGroup/>
</main>

<style>
    main {
        width: 100%;
        height: 100%;
        margin: 0;
    }

    .index-container {
        margin-top: 50px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>
