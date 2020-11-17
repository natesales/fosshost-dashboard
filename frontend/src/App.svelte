<script>
    import Sidebar from "./components/Sidebar.svelte";
    import Navbar from "./components/Navbar.svelte";
    import Footer from "./components/Footer.svelte";
    import Profile from "./components/Profile.svelte";
    import {Page} from "./stores.js";
    import RequestForm from "./components/RequestForm.svelte";
    import Dashboard from "./components/Dashboard.svelte";
    import Login from "./components/Login.svelte";
    import Register from "./components/Register.svelte";
    import SnackbarGroup from "./components/SnackbarGroup.svelte";

    // const urlParams = new URLSearchParams(window.location.search);
    // export let page = urlParams.get("page") ? urlParams.get("page") : "dashboard"

    // Set title
    $: {
        document.title = $Page.charAt(0).toUpperCase() + $Page.slice(1) + " | FOSSHOST"
    }

</script>

<main>
    {#if $Page === "login"}
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
</style>