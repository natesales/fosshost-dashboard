<script>
    import Sidebar from "./components/Sidebar.svelte";
    import Navbar from "./components/Navbar.svelte";
    import Footer from "./components/Footer.svelte";
    import StatBoxes from "./components/StatBoxes.svelte";
</script>

<main>
    <div class="wrapper">
        <Sidebar/>
        <div class="main-panel">
            <Navbar projectName="delivr"/>
            <div class="content">
                <div class="container-fluid">
                    <StatBoxes/>
                    <div class="row">
                        <div class="col-lg-12">
                            <div class="card">
                                <div class="card-header card-header-danger">
                                    <h4 class="card-title">
                                        Virtual Machines
                                    </h4>
                                    <p class="card-category">
                                        <u><a href="/request">Request a new
                                            VM</a></u>
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
                                            <th>Location</th>
                                            <th>Control</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td>test-machine.fosshost.org</td>
                                            <td><i class="material-icons color-green">done</i></td>
                                            <td>192.168.0.25<br/>2001:db8::1</td>
                                            <td>
                                                4 Cores / 4GB RAM /
                                                100GB Disk / Debian
                                                10.5.0
                                            </td>
                                            <td>
                                                <img alt="Country Icon" class="padding-right" src="https://www.countryflags.io/gb/flat/32.png"/>LAX1
                                            </td>
                                            <td>
                                                <input
                                                        class="control-button button-green"
                                                        onclick="alert('Starting')"
                                                        type="button"
                                                        value="Start"/>
                                                <input
                                                        class="control-button button-red"
                                                        onclick="alert('Stop')"
                                                        type="button"
                                                        value="Stop"/>
                                                <input
                                                        class="control-button button-blue"
                                                        onclick="alert('Console')"
                                                        type="button"
                                                        value="Console"/>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <Footer/>
        </div>
    </div>
</main>
