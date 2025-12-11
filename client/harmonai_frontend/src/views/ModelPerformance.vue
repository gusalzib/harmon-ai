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

                    <h5>{{ $t('admin.model.version') }}: V{{ report.version }}</h5>
                    <p>{{ $t('admin.model.accuracy') }}: <strong>{{ report.accuracy }}%</strong></p>
                    <p>{{ $t('admin.model.date') }}: {{ report.date }}</p>

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
                    <div v-html="this.selectedReport.htmlContent" class="report-html-content"></div>
                </div>

                <div class="report-panel comparison-report" v-if="this.comparisonReport">
                    <h4>{{ $t('admin.model.comparisonTo') }} V{{ this.comparisonReport.version }}</h4>
                    <div v-html="this.comparisonReport.htmlContent" class="report-html-content"></div>
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

            url: 'http://localhost:8000/admin/model-performance',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000,

            selectedReport: null,
            comparisonReport: null, 
            // availableReports: [
            //     // these are just dummy reports
            //     {version: '2.1', accuracy: 86.0, date: '2025-12-10', htmlContent: '<p>Report content for V2.1</p>'},
            //     {version: '2.0', accuracy: 75.0, date: '2025-11-25', htmlContent: '<p>Report content for V2.0</p>'},
            //     {version: '1.9', accuracy: 70.0, date: '2025-11-10', htmlContent: '<p>Report content for V1.9</p>'},
            // ], 
availableReports: [
  {
    version: '2.1',
    accuracy: 86.0,
    date: '2025-12-10',
    htmlContent: `
      <section>
        <h2>Model Performance Report – Version 2.1</h2>
        <p><strong>Release date:</strong> 2025-12-10</p>

        <h3>Overview</h3>
        <p>
          Version <strong>2.1</strong> focuses on improving classification robustness,
          especially for underrepresented classes. It introduces additional
          data augmentation and a tuned learning rate schedule.
        </p>

        <h3>Key Metrics</h3>
        <table border="0" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
          <thead>
            <tr style="border-bottom:1px solid #ddd;">
              <th align="left">Metric</th>
              <th align="left">Value</th>
              <th align="left">Change vs 2.0</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Accuracy</td>
              <td>86.0%</td>
              <td>+11.0 pts</td>
            </tr>
            <tr>
              <td>Precision (macro)</td>
              <td>84.2%</td>
              <td>+8.5 pts</td>
            </tr>
            <tr>
              <td>Recall (macro)</td>
              <td>83.1%</td>
              <td>+9.3 pts</td>
            </tr>
            <tr>
              <td>F1-score (macro)</td>
              <td>83.6%</td>
              <td>+8.9 pts</td>
            </tr>
          </tbody>
        </table>

        <h3>Dataset & Evaluation</h3>
        <ul>
          <li><strong>Train set:</strong> 80,000 samples</li>
          <li><strong>Validation set:</strong> 10,000 samples</li>
          <li><strong>Test set:</strong> 10,000 samples</li>
          <li>Same data split as versions 1.9 and 2.0 for comparability.</li>
        </ul>

        <h3>Improvements vs 2.0</h3>
        <ul>
          <li>Reduced false positives on minority classes by ~14%.</li>
          <li>More stable predictions on noisy inputs.</li>
          <li>Inference latency unchanged (P95 around 120ms).</li>
        </ul>

        <h3>Known Limitations</h3>
        <ul>
          <li>Still sensitive to heavily out-of-distribution inputs.</li>
          <li>Performance on class "C3" is below target (F1 &lt; 0.75).</li>
        </ul>

        <h3>Recommendations</h3>
        <ol>
          <li>Use 2.1 as the default production model for all new deployments.</li>
          <li>Monitor performance on minority classes weekly for the first month.</li>
          <li>Plan a follow-up release focused on class "C3" misclassifications.</li>
        </ol>
      </section>
    `
  },
  {
    version: '2.0',
    accuracy: 75.0,
    date: '2025-11-25',
    htmlContent: `
      <section>
        <h2>Model Performance Report – Version 2.0</h2>
        <p><strong>Release date:</strong> 2025-11-25</p>

        <h3>Overview</h3>
        <p>
          Version <strong>2.0</strong> is the first release in the 2.x line.
          It introduced a new architecture with deeper layers and a revised feature
          extraction block, aiming to improve generalization over version 1.9.
        </p>

        <h3>Key Metrics</h3>
        <table border="0" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
          <thead>
            <tr style="border-bottom:1px solid #ddd;">
              <th align="left">Metric</th>
              <th align="left">Value</th>
              <th align="left">Change vs 1.9</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Accuracy</td>
              <td>75.0%</td>
              <td>+5.0 pts</td>
            </tr>
            <tr>
              <td>Precision (macro)</td>
              <td>73.5%</td>
              <td>+4.1 pts</td>
            </tr>
            <tr>
              <td>Recall (macro)</td>
              <td>72.8%</td>
              <td>+3.9 pts</td>
            </tr>
            <tr>
              <td>F1-score (macro)</td>
              <td>73.1%</td>
              <td>+4.0 pts</td>
            </tr>
          </tbody>
        </table>

        <h3>Highlights</h3>
        <ul>
          <li>Noticeable uplift in overall accuracy over version 1.9.</li>
          <li>Better handling of medium-frequency classes.</li>
          <li>Some degradation for rare classes due to underfitting.</li>
        </ul>

        <h3>Deployment Notes</h3>
        <ul>
          <li>Passed all baseline regression tests.</li>
          <li>Shadow-tested for 7 days before full rollout.</li>
          <li>No major incidents reported during initial deployment.</li>
        </ul>

        <h3>Next Steps</h3>
        <p>
          The main focus areas identified from version 2.0 were:
        </p>
        <ul>
          <li>Improve recall on rare classes.</li>
          <li>Reduce overconfidence on borderline predictions.</li>
          <li>Refine training data to balance underrepresented segments.</li>
        </ul>
      </section>
    `
  },
  {
    version: '1.9',
    accuracy: 70.0,
    date: '2025-11-10',
    htmlContent: `
      <section>
        <h2>Model Performance Report – Version 1.9</h2>
        <p><strong>Release date:</strong> 2025-11-10</p>

        <h3>Overview</h3>
        <p>
          Version <strong>1.9</strong> is the last stable release from the 1.x line.
          It served as the baseline model for the 2.x redesign and is still useful
          as a reference for long-term performance comparisons.
        </p>

        <h3>Key Metrics</h3>
        <table border="0" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
          <thead>
            <tr style="border-bottom:1px solid #ddd;">
              <th align="left">Metric</th>
              <th align="left">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Accuracy</td>
              <td>70.0%</td>
            </tr>
            <tr>
              <td>Precision (macro)</td>
              <td>69.4%</td>
            </tr>
            <tr>
              <td>Recall (macro)</td>
              <td>68.2%</td>
            </tr>
            <tr>
              <td>F1-score (macro)</td>
              <td>68.8%</td>
            </tr>
          </tbody>
        </table>

        <h3>Strengths</h3>
        <ul>
          <li>Stable behavior in production over an extended period.</li>
          <li>Predictable performance on majority classes.</li>
          <li>Low operational risk and well-understood failure modes.</li>
        </ul>

        <h3>Limitations</h3>
        <ul>
          <li>Limited capacity for complex patterns compared to 2.x models.</li>
          <li>Underperforms on rare classes and noisy inputs.</li>
          <li>Higher calibration error (poor probability estimates).</li>
        </ul>

        <h3>Role in the Lifecycle</h3>
        <p>
          Version 1.9 is retained mainly for:
        </p>
        <ul>
          <li>Historical comparisons and A/B experiments.</li>
          <li>Fallback in case of severe regressions in newer models.</li>
          <li>Benchmarking the impact of new data and architectures.</li>
        </ul>
      </section>
    `
  }
]


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable


    },
    methods: {
        fetchReportList() {
            
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
    }
}
</script>