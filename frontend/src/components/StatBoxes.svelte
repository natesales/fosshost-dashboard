<script>
    import {Page, Counters} from "../stores.js";
</script>

<main>
    <div class="row">
        <div class="col-lg-3 col-md-6 col-sm-6">
            <div class="card card-stats">
                <div class="card-header card-header-info card-header-icon">
                    <div class="card-icon"><i class="material-icons">dns</i></div>
                    <p class="card-category">VMs</p>
                    <h3 class="card-title">{$Counters.vms}</h3>
                </div>
                <div class="card-footer">
                    <div class="stats">
                        <i class="material-icons">dns</i>
                        <a on:click={() => {$Page = "request"}}>Infrastructure Request</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6 col-sm-6">
            <div class="card card-stats">
                <div class="card-header card-header-danger card-header-icon">
                    <div class="card-icon"><i class="material-icons">lock</i></div>
                    <p class="card-category">SSH Keys</p>
                    <h3 class="card-title">{$Counters.keys}</h3>
                </div>
                <div class="card-footer">
                    <div class="stats">
                        <i class="material-icons">lock</i>
                        <a on:click={() => {$Page = "profile"}}>Profile Settings</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6 col-sm-6">
            <div class="card card-stats">
                <div class="card-header card-header-warning card-header-icon">
                    <div class="card-icon">
                        <i class="material-icons">public</i>
                    </div>
                    <p class="card-category">Locations</p>
                    <h3 class="card-title">{$Counters.locations}</h3>
                </div>
                <div class="card-footer">
                    <div class="stats">
                        <i class="material-icons">dns</i>
                        <a on:click={() => {$Page = "request"}}>Infrastructure Request</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6 col-sm-6">
            <div class="card card-stats">
                <div class="card-header card-header-icon">
                    <div class="card-icon">
                        <i class="material-icons">info</i>
                    </div>
                    <p class="card-category">Alerts</p>
                    <h3 class="card-title">{$Counters.alerts}</h3>
                </div>
                <div class="card-footer">
                    <div class="stats">
                        <i class="material-icons">update</i>
                        <a onclick="location.reload()">Refresh</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>