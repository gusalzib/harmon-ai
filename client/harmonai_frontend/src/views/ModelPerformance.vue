<template>
    <div class="model-performance-section" id="performance-report">
        <h3>{{ $t('admin.model.modelPerformanceReports') }}</h3>

        <div class="reports-container">
            <div  class="report-list-panel">
                <h4>{{ $t('admin.model.availableVerions') }}</h4>

                <div v-for="report in this.availableReports" :key="report.version" :class="['report-card', {
                    'selected': this.selectedReport && this.selectedReport.version === report.version,
                    'compared': this.comparisonReport && this.comparisonReport.version == report.version
                }]" @click="selectReport(report)">

                <!-- 'report-card' is always true and this is the base class. Hoever, we need to add classes like selected and compared based on what the user clicks
                      or slectes. So:
                      'selected' is added if  this.selectedReport && this.selectedReport.version === report.version. We ensure that the selectedReport is not null, then 
                      we check if the current loop iteration matches the version of the selected report. This is because is a report is selected, we need to highlight the card
                      whose version matches the selected report's version.
                      'compared' is similar to selected, this class marks the report card used for cmparsion. if the user has chosen a second report for side-by-side
                      comparison, this class signlas which report is playing the comparedTo role.  -->

                    <h5>{{ $t('admin.model.name') }}: {{ report.name }}</h5>
                    <h5>{{ $t('admin.model.version') }}: V{{ report.version }}</h5>
                    


                    <!-- since the parent div hax @click="selectReport" we add @click.stop here to make sure that the button click only triggers setComparisonReport() and not
                          selectReport(). 
                          .stop prevents the click from propagating to the parent element-->
                    <button v-if="this.selectedReport && this.selectedReport.version !== report.version" class="standard-btn compare-btn" @click.stop="setComparisonReport(report)">
                        {{ $t('buttons.comparebutton') }}
                    </button>
                </div>
            </div>

            <!-- :class="['report-display-area', {'split-view': this.comparisonReport}] 
                We add  report-display-area as the base class and only add the slpit view if the comparisonReport variable is true(is not null)-->
            <div v-if="this.selectedReport" :class="['report-display-area', {'split-view': this.comparisonReport}]">
                <button class="standard-btn close-report-btn" @click="closeComparison">
                    &times; {{ $t('buttons.closeButton') }}
                </button>

                <div class="report-panel primary-report">
                    <h4>{{ $t('admin.model.reportFor') }} V{{ this.selectedReport.version }}</h4>
                    <button class="standard-btn update-model-btn" @click="updateModel">
                        {{ $t('buttons.deployModel') || 'Deploy Model' }}
                    </button>
                     <iframe :src="this.selectedReport.url" frameborder="0"></iframe>
                </div>

                <div class="report-panel comparison-report" v-if="this.comparisonReport">
                    <h4>{{ $t('admin.model.comparisonTo') }} V{{ this.comparisonReport.version }}</h4>
                    <iframe :src="this.comparisonReport.url" frameborder="0"></iframe>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'
import { getCsrfToken } from '@/utils/csrfTokenUtils';


export default {
    name: 'ModelPerformance',
    data() {
        return {

            url: '',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000,

            selectedReport: null,
            comparisonReport: null, 
            availableReports: [],
        }
    },
    mounted() {
        this.url = `${import.meta.env.VITE_API_URL || "http://34.51.250.115"}/admins/report/`
        this.toast = useToast(); // initiate a toast variable
        this.fetchReportList();

    },
    methods: {
        async fetchReportList() {
            this.toast.info(this.$t('admin.model.fetchingReports'), { timeout: false });

            try {

                const response = await axios.get(this.url)

                const reportData = response.data.reports;

                if (reportData && reportData.length > 0) {
                    this.availableReports = reportData;


                    this.toast.clear();
                    this.toast.success(this.$t('admin.model.reportsLoaded'));
                } else {
                    this.toast.clear();
                    this.toast.warning(this.$t('admin.model.noReportsFound'));
                }

            } catch (error) {
                this.toast.clear();
                const errorMessage = error.response?.data?.message || error.message;
                this.toast.error(`${this.$t('admin.model.reportFetchingError')} ${errorMessage}`);
                console.error('Report fetch error: ', error)
            }
        },
        // add a second report to the primary report for comparison in a split-view layout
        setComparisonReport(report) {

            if (this.selectedReport && this.selectedReport.version === report.version) {
                this.toast.warning(this.$t('admin.model.cannotCompareSameReport'));
                return;
            }

            this.comparisonReport = report;
            this.toast.info(this.$t('admin.model.comparisonActive').replace('{version}', report.version));


        },
        selectReport(report) {
            // if the user clicks the report that is currently being compared, swap them 
            if (this.comparisonReport && this.comparisonReport.version === report.version) {
                let temp = this.selectedReport;
                this.selectedReport = this.comparisonReport;
                this.comparisonReport = temp;
            } else {
                this.selectedReport = report;
                this.comparisonReport = null; // we exit the comparison view if a new primary report is selected
            }
        },
        // exit the split view
        closeComparison() {
            this.comparisonReport = null;
            this.selectedReport = null;
        },

        async updateModel() {
            if (!this.selectedReport) return;

            this.toast.info(this.$t('admin.model.updatingModel') || "Updating model...", { timeout: false });

            try {
                const baseUrl = import.meta.env.VITE_API_URL || "http://34.51.250.115.nip.io";
                // Call the backend endpoint that triggers update_model.py
                const response = await axios.post(`${baseUrl}/admins/update/`, {
                    modelName: this.selectedReport.name
                });

                this.toast.clear();
                this.toast.success(this.$t('admin.model.modelUpdateSuccess') || "Model updated successfully");
            } catch (error) {
                this.toast.clear();
                this.toast.error(this.$t('admin.model.modelUpdateFailed') || "Failed to update model");
                console.error(error);
            }
        }
    }
}
</script>

<style scoped>
.update-model-btn {
    background-color: #28a745;
    color: white;
    border: none;
}
.update-model-btn:hover {
    background-color: #218838;
}
</style>