<main>
    <div class="col-md-8">
        <div class="card">
            <div class="card-header card-header-danger">
                <h4 class="card-title">Infrastructure Request</h4>
                <p class="card-category">Submit a request for new infrastructure</p>
            </div>
            <div class="card-body danger">
                <form>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group bmd-form-group">
                                <label class="bmd-label-static">Service</label>
                                <select class="form-control">
                                    <option value="vps">VPS</option>
                                    <option value="domain">Domain</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group">
                                <label>More Information</label>
                                <div class="form-group bmd-form-group">
                                    <label class="bmd-label-floating">More information about this request...</label>
                                    <textarea class="form-control red-banner" rows="6"></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="btn btn-primary pull-right red-button" type="submit">Submit</button>
                    <div class="clearfix"></div>
                </form>
            </div>
        </div>
    </div>
</main>

<style>
    .red-banner {
        background-image: linear-gradient(to top, #e53935 2px, rgba(156, 39, 176, 0) 2px), linear-gradient(to top, #d2d2d2 1px, rgba(210, 210, 210, 0) 1px);
    }

    .red-button:hover {
        box-shadow: 0 14px 26px -12px #e53935, 0 4px 23px 0px rgba(0, 0, 0, 0.12), 0 8px 10px -5px #ff5350;
        border-color: #ff5350;
        background-color: #ff5350;
    }
</style>
