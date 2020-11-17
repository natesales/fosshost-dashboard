<script>
    import { Page } from "../stores.js";
</script>

<main>
    <div class="sidebar" data-background-color="white" data-color="danger" data-image="/static/assets/img/sidebar-4.jpg">
        <div class="logo">
            <a class="simple-text logo-normal" on:click={() => {$Page = "dashboard"}}>
                <img src="/static/assets/img/logo.png" width="75%"/>
            </a>
        </div>

        <div class="sidebar-wrapper">
            <ul class="nav">
                <li class="nav-item {$Page === 'dashboard' ? 'active' : ''}">
                    <a class="nav-link" on:click={() => {$Page = "dashboard"}}>
                        <i class="material-icons">dashboard</i>
                        <p>Dashboard</p>
                    </a>
                </li>
                <li class="nav-item {$Page === 'profile' ? 'active' : ''}">
                    <a class="nav-link" on:click={() => {$Page = "profile"}}>
                        <i class="material-icons">person</i>
                        <p style="text-transform: none">Profile and Security</p>
                    </a>
                </li>
                <li class="nav-item {$Page === 'request' ? 'active' : ''}">
                    <a class="nav-link" on:click={() => {$Page = "request"}}>
                        <i class="material-icons">add_circle</i>
                        <p>Infrastructure Request</p>
                    </a>
                </li>
            </ul>
        </div>
    </div>
</main>
