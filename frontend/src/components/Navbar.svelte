<script>
    export let projectName;
</script>

<main>
    <nav class="navbar navbar-expand-lg navbar-transparent navbar-absolute fixed-top ">
        <div class="container-fluid">
            <div class="navbar-wrapper">
                <p class="navbar-brand">
                    Welcome to Fosshost, <span class="color-red">{ projectName }</span>!
                </p>
            </div>
            <button
                    aria-controls="navigation-index"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                    class="navbar-toggler"
                    data-toggle="collapse"
                    type="button">
                <span class="sr-only">Toggle navigation</span>
                <span class="navbar-toggler-icon icon-bar"/>
                <span class="navbar-toggler-icon icon-bar"/>
                <span class="navbar-toggler-icon icon-bar"/>
            </button>
            <div
                    class="collapse navbar-collapse justify-content-end">
                <ul class="navbar-nav">
                    <li class="nav-item dropdown">
                        <a
                                aria-expanded="false"
                                aria-haspopup="true"
                                class="nav-link"
                                data-toggle="dropdown"
                                href="javascript:"
                                id="navbarDropdownProfile">
                            <i class="material-icons">person</i>
                            <p class="d-lg-none d-md-block">
                                Account
                            </p>
                        </a>
                        <div
                                aria-labelledby="navbarDropdownProfile"
                                class="dropdown-menu dropdown-menu-right">
                            <a
                                    class="dropdown-item"
                                    href="/profile">Profile</a>
                            <div class="dropdown-divider"></div>
                            <a
                                    class="dropdown-item"
                                    href="/logout">Log out</a>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</main>