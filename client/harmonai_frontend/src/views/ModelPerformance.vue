<!--

Authors of code:
- Ibrahim Alzoubi - gusalzib@student.gu.se - alzoubi@chalmers.se
- Muhamad Jawad Ahmad 

-->
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
                    <p>Total number of examples: {{this.overall_examples}}</p>
                    <h3>Overall Accuracy of Keys and Qualities</h3>
                    <div class="pie-chart-container">
                        <Pie
                            id="Overall-Accuracy"
                            :options="chartOptions"
                            :data="overall_accuracy_chartData"
                        />
                    </div>

                    <h3>Keys Accuracy</h3>
                    <div class="pie-chart-container">
                        <Pie
                            id="Overall-Accuracy"
                            :options="chartOptions"
                            :data="keys_accuracy_chartData"
                        />
                    </div>

                    <h3>Qualities Accuracy</h3>
                    <div class="pie-chart-container">
                        <Pie
                            id="Overall-Accuracy"
                            :options="chartOptions"
                            :data="qualities_accuracy_chartData"
                        />
                    </div>                    
                    
                </div>

                <div class="report-panel comparison-report" v-if="this.comparisonReport">
                    <h4>{{ $t('admin.model.comparisonTo') }} V{{ this.comparisonReport.version }}</h4>

                    <button class="standard-btn update-model-btn" @click="updateModel">
                        {{ $t('buttons.deployModel') || 'Deploy Model' }}
                    </button>
                    <p>Total number of examples: {{this.comparison_overall_examples}}</p>
                    <h3>Overall Accuracy of Keys and Qualities</h3>
                    <div class="pie-chart-container">
                        <Pie
                            id="Overall-Accuracy"
                            :options="chartOptions"
                            :data="comparison_overall_accuracy_chartData"
                        />
                    </div>

                    <h3>Keys Accuracy</h3>
                    <div class="pie-chart-container">
                        <Pie
                            id="Overall-Accuracy"
                            :options="chartOptions"
                            :data="comparison_keys_accuracy_chartData"
                        />
                    </div>

                    <h3>Qualities Accuracy</h3>
                    <div class="pie-chart-container">
                        <Pie
                            id="Overall-Accuracy"
                            :options="chartOptions"
                            :data="comparison_qualities_accuracy_chartData"
                        />
                    </div>                    
                    
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'
import { getCsrfToken } from '@/utils/csrfTokenUtils';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement } from 'chart.js'
import {Bar, Pie, Line} from 'vue-chartjs';
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, LineElement, ArcElement, MatrixController, MatrixElement)

export default {
    name: 'ModelPerformance',
    components: {
        Bar,
        Pie,
        Line
    },
    data() {
        return {
            url: '',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000,

            selectedReport: null,
            comparisonReport: null, 
            availableReports: [],

            // variable for JSON reports
            json_reports: [],
            overall_accuracy: 0.0,
            keyAccuracy: 0.0,
            qualityAccuracy: 0.0,
            overall_examples: 0.0,


            comparison_overall_accuracy: 0.0,
            comparison_keyAccuracy: 0.0,
            comparison_qualityAccuracy: 0.0,
            comparison_overall_examples: 0.0,

            accuracy_per_key: [],
            examples_per_key: [],
            accuracy_per_quality: [],
            examples_per_quality: [],
            key_labels: [],
            quality_labels: [],
            
            chartOptions: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                    // tooltip is when we hover over the data points in the chart. It will show more detailed information
                        tooltip: {
                            enabled: true, // enable tooltips
                            backgroundColor: 'rgba(0,0,0,0.7)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            titleFont: { size: 14 },
                            bodyFont: { size: 12 },
                        }
                    }
                },
        }
    },
    computed: {
        overall_accuracy_chartData() {
            return {
                labels: ['Accurate Predictions', 'Inaccurate Predictions'],
                datasets: [{
                    label: 'Accuracy Metrics',
                    data: [this.overall_accuracy, 100 - this.overall_accuracy],
                    backgroundColor: ['#4A306D', '#CBAADE']
                }]
            }
        }, 
        keys_accuracy_chartData() {
            return {
                labels: ['Accurate Predictions', 'Inaccurate Predictions'],
                datasets: [{
                    label: 'Accuracy Metrics',
                    data: [this.keyAccuracy, 100 - this.keyAccuracy],
                    backgroundColor: ['#4A306D', '#CBAADE']
            }]
        }
    }, 
        qualities_accuracy_chartData() {
            return {
                labels: ['Accurate Predictions', 'Inaccurate Predictions'],
                datasets: [{
                    label: 'Accuracy Metrics',
                    data: [this.qualityAccuracy, 100 - this.qualityAccuracy],
                    backgroundColor: ['#4A306D', '#CBAADE']
        }]
    }
    }, 


        comparison_overall_accuracy_chartData() {
            return {
                labels: ['Accurate Predictions', 'Inaccurate Predictions'],
                datasets: [{
                    label: 'Accuracy Metrics',
                    data: [this.comparison_overall_accuracy, 100 - this.comparison_overall_accuracy],
                    backgroundColor: ['#4A306D', '#CBAADE']
                }]
            }
        }, 
        comparison_keys_accuracy_chartData() {
            return {
                labels: ['Accurate Predictions', 'Inaccurate Predictions'],
                datasets: [{
                    label: 'Accuracy Metrics',
                    data: [this.comparison_keyAccuracy, 100 - this.comparison_keyAccuracy],
                    backgroundColor: ['#4A306D', '#CBAADE']
            }]
        }
    }, 
        comparison_qualities_accuracy_chartData() {
            return {
                labels: ['Accurate Predictions', 'Inaccurate Predictions'],
                datasets: [{
                    label: 'Accuracy Metrics',
                    data: [this.comparison_qualityAccuracy, 100 - this.comparison_qualityAccuracy],
                    backgroundColor: ['#4A306D', '#CBAADE']
        }]
    }
    }, 


            accuracy_per_key_chartData() {
            return {
                labels: ['Key', 'Accuracy'],
                datasets: [{
                    label: 'Accuracy per Key Metrics',
                    data: [this.key_labels, this.accuracy_per_key],
                    backgroundColor: ['#4A306D', '#CBAADE']
        }]
    }
    }, 
            examples_per_key_chartData() {
            return {
                labels: ['Accurate Predictions', 'Inaccurate Predictions'],
                datasets: [{
                    label: 'Accuracy Metrics',
                    data: [this.key_labels, this.examples_per_key],
                    backgroundColor: ['#4A306D', '#CBAADE']
        }]
    }
    },
    
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
            this.comparison_keyAccuracy = this.comparisonReport.content.overall_metrics.key.accuracy * 100;

            this.comparison_qualityAccuracy = this.comparisonReport.content.overall_metrics.quality.accuracy * 100;
            console.log("quality accuracy: ", this.qualityAccuracy);

            this.comparison_overall_accuracy = ( ( this.comparison_keyAccuracy + this.comparison_qualityAccuracy ) / 2 )
            console.log("total accuracy = " + this.comparison_overall_accuracy)

            this.comparison_overall_examples = this.comparisonReport.content.overall_metrics.total_examples;
            console.log("total examples = " + this.comparison_overall_examples)
            this.getOverAllAccuracy()
        },

        // Why was this function not async from the start? 
        async selectReport(report) {
            // if the user clicks the report that is currently being compared, swap them 
            console.log("the report url is " + report.url)
            if (this.comparisonReport && this.comparisonReport.version === report.version) {
                let temp = this.selectedReport;
                this.selectedReport = this.comparisonReport;
                this.comparisonReport = temp;


            } else {
                this.selectedReport = report;
                
                this.comparisonReport = null; // we exit the comparison view if a new primary report is selected
                // this.json_reports = this.getReportJSON(report.content)

                await this.$nextTick();
                console.log("the report: " + JSON.stringify(this.selectedReport.content));

                console.log("key matrix: " + JSON.stringify(this.selectedReport.content.overall_metrics.key.confusion_matrix));
                console.log("key class_labels " + JSON.stringify(this.selectedReport.content.overall_metrics.key.class_labels));
                const labels = this.selectedReport.content.overall_metrics.key.class_labels;
                console.log("the second class label is: " + labels[1])
                this.getOverAllAccuracy(); 
    
            }
        },

        async getOverAllAccuracy() {
            try {
                // await this.$nextTick();

                this.keyAccuracy = this.selectedReport.content.overall_metrics.key.accuracy * 100;
                console.log("key accuracy: ", this.keyAccuracy);
                console.log("the type of key accuracy is ", typeof this.keyAccuracy)

                this.qualityAccuracy = this.selectedReport.content.overall_metrics.quality.accuracy * 100;
                console.log("quality accuracy: ", this.qualityAccuracy);

                this.overall_accuracy = ( ( this.keyAccuracy + this.qualityAccuracy ) / 2 )
                console.log("total accuracy = " + this.overall_accuracy)

                this.overall_examples = this.selectedReport.content.overall_metrics.total_examples;
                console.log("total examples = " + this.overall_examples)
            }
            catch (error) {
                console.log("Error", error)
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