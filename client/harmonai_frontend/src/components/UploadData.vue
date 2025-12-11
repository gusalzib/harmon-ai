<template>
    <div class="upload-data-section" id="upload" v-if="activeSection === 'dataUpload'">
        <h3>{{ $t('admin.model.uploadData') }}</h3>

        <div class="token-varification">
        <button type="button" class="standard-btn token-varification-btn" @click="oauthSignIn">
            <span v-if="!this.accessToken">
            {{ $t('admin.model.connectGCS') }}
            </span>
            <span v-else>
            {{ $t('admin.model.gcsConnected') }}
            </span>
        </button>
        <span v-if="this.accessToken" class="token-status">
            &nbsp;&nbsp;{{ $t('admin.model.gcsTokenActive') }}
        </span>
        </div>
        <br>
        <br>
        <form @submit.prevent="submitDatasetFolder" class="dataset-upload-form">
            <div class="form-container">
                <label for="dataset-upload">
                    {{ $t('admin.model.selectFileLabel') }}
                </label>

                <input 
                    type="file"
                    id="dataset-file"
                    ref="fileInput"
                    @change="handleFolderSubmit" webkitdirectory
                    directory
                    required
                    >

                    <p v-if="this.fileName" class="file-status">
                        {{ $t('admin.model.fileSelected') }}: <strong>{{ this.fileName }}</strong>
                        <br>
                        {{ $t('admin.model.fileSize') }}: <strong>{{ this.fileSize }} MB</strong>
                    </p>
            </div>

            <button type="submit" class="standard-btn submit-upload-btn" :disabled="this.isUploading">
                <span v-if="this.isUploading">
                    {{ $t('admin.model.uploadingButton') }}
                </span>
                <span v-else>
                    {{ $t('buttons.uploadButton') }}
                </span>
            </button>
        </form>
    </div>
</template>

<script>
import { getCsrfToken } from '@/utils/csrfTokenUtils';
import axios from 'axios';
import JSZip from 'jszip';
import { useToast } from 'vue-toastification'

// google cloud conntection variables
const GCS_BUCKET_NAME = import.meta.env.VITE_GCS_BUCKET_NAME;
const GCS_CLIENT_ID = import.meta.env.VITE_GCS_CLIENT_ID;
const scope = import.meta.env.VITE_SCOPE;
const REDIRECT_URL = window.location.origin;

export default {
    name: 'UploadData',
    data() {
        return {
            toast: null, // declare a toast variable to be used with toastification library for notifications
            activeSection: 'dataUpload', //this controls which section in visible to the user at any time.
            // selectedFile: null,
            fileName: '', 
            fileSize: 0,
            isUploading: false, // monitors whether the file upload is ongoing

            selectedFiles: [], // an array that saves selected files (folder)

            accessToken: null, // stores the access token we get from the google cloud 


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable

        /**
         * The access token is stored in the localstorage when we mount the application in the main.js. 
         * here we simply read  it from the local storage.
         */
        const gcs_token = localStorage.getItem('gcsAccessToken');
        if (gcs_token) {
            this.accessToken = gcs_token;

        }

    },
    methods: {

        handleFolderSubmit(event) {
            // we store the file object from the upload event 
            const files = event.target.files
            this.selectedFiles = [];
            this.fileSize = 0; // stores the overall size of all files in the dataset

            if (files.length === 0) {
                this.toast.error(this.$t('admin.model.noFileError'));
                return;
            }

            let totalSize = 0;

            // add all selected files to the selectedFiles array 
            for (let index = 0; index < files.length; index++) {
                const file = files[index];
                    this.selectedFiles.push(file);
                    totalSize = totalSize + file.size
            }

            // we divide by 1024 squared because we are converting from bytes to kilobytes and then from kilobytes to megabytes
            this.fileSize = totalSize / (1024 * 1024);
            
            // we tell the user how many files exist inside the folder they selected and how big are they combined
            this.toast.info(this.$t('admin.model.folderSelected') + `${this.selectedFiles.length} `+ this.$t('admin.model.files') +` (${this.fileSize.toFixed(2)} MB)`)


        },
        async zipDataset() {
            // https://www.cjoshmartin.com/blog/creating-zip-files-with-javascript?project_audience=DEV

            const zip = new JSZip();

            for (const file of this.selectedFiles) {
                /**
                 * file.webkitRelativePath will keep the file path if it exists
                 * this is an example of how the file.webkitRelativePath will preserve the file path when selected
                 * billboard-2.0.1-mirex/1300/majmin.lab
                 * billboard-2.0.1-mirex/1300/majmin7.lab
                 * billboard-2.0.1-mirex/1300/majmin7inv.
                 * 
                 * https://developer.mozilla.org/en-US/docs/Web/API/File/webkitRelativePath
                 */
                const pathInZipedFolder = file.webkitRelativePath || file.name;

                zip.file(pathInZipedFolder, file);
                
            }

            // timeout disabled so that the loading toast stays until we clear it when the folder is zipped
            this.toast.info(this.$t('admin.model.creatingZippedFile'), { timeout: false });

            const blob = await zip.generateAsync({ type: 'blob' });
            this.toast.clear();

            // we name the file dataset_ and we concatinate that with the Date of today and finish it off with .zip extention
            const zipFileName = `dataset_${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')}.zip`;

            // we finally convert it to normal file format because that is what the upload method is expecting
            return new File([blob], zipFileName, { type: 'application/zip' });

        },
        oauthSignIn() {
            // https://dev.to/akirakashihara/how-to-upload-files-to-google-cloud-storage-using-javascript-on-only-the-browser-11ei
            var oauth2Endpoint = "https://accounts.google.com/o/oauth2/v2/auth"; 
            // Create <form> element to submit parameters to OAuth 2.0 endpoint.
            var form = document.createElement("form");
            form.setAttribute("method", "GET"); // Send as a GET request.
            form.setAttribute("action", oauth2Endpoint);

            // Parameters to pass to OAuth 2.0 endpoint.
            var params = {
                client_id: GCS_CLIENT_ID,
                redirect_uri: REDIRECT_URL,
                response_type: "token",
                scope: scope,
                include_granted_scopes: "true",
                state: "pass-through value",
            };

            // Add form parameters as hidden input values.
            for (var p in params) {
                var input = document.createElement("input");
                input.setAttribute("type", "hidden");
                input.setAttribute("name", p);
                input.setAttribute("value", params[p]);
                form.appendChild(input);
            }

            // Add form to page and submit it to open the OAuth 2.0 endpoint.
            document.body.appendChild(form);
            form.submit();
        },
        // upload to Google Cloud Storage
        async uploadToGCS(file) {
            // we block the request if there is not token
            if (!this.accessToken) {
                this.toast.error(this.$t('admin.model.noAccessToken'));
                // reject the request (I tried a normal 'return;' but it did not work so i had to pull out the big guns)
                throw new Error(this.$t('admin.model.noAccessToken'));
            }

            const file_name = file.name;
            /**
             * Any kind of binary data that doesn't fall explicitly into one of the other types; either data that will be executed or 
             * interpreted in some way or binary data that requires a specific application or category of application to use. 
             * Generic binary data (or binary data whose true type is unknown) is application/octet-stream.
             * https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types 
             */
            const content_type = file.type || 'application/octet-stream';

            this.toast.info(this.$t('admin.model.uploading') + `${file_name}` + this.$t('admin.model.directlyToGCS'), { timeout: false });

            return new Promise((resolve, reject) => {
                //https://developer.mozilla.org/en-US/docs/Web/API/FileReader
                const reader = new FileReader();

                reader.onload = async (event) => {
                    const bytes = event.target.result;

                    // I needed to prefix the file name with the data/ so that the uploaded folders are sent to the data/ directory in the cloud
                    const prefixed_filename = `data/${file.name}`;
                    try {
                        let response = await fetch(`https://storage.googleapis.com/upload/storage/v1/b/${GCS_BUCKET_NAME}/o?uploadType=media&name=${encodeURIComponent(prefixed_filename)}`,
                            {
                                method: "POST",
                                headers: {
                                    "Content-Type": content_type,
                                    "Authorization": `Bearer ${this.accessToken}`,
                                },
                                body: bytes,
                            });

                        let result = await response.json();

                        if (result.mediaLink) {
                            this.toast.success(this.$t('admin.model.fileUploadedToGCSsuccessfully') + file_name);
                            resolve(result.mediaLink);

                        } else {
                            this.toast.error(this.$t('admin.model.fileUploadedToGCSFailed'));
                            reject(this.$t('admin.model.fileUploadedToGCSFailed') + JSON.stringify(result));
                        }

                    } catch (error) {
                        this.toast.error(this.$t('notification.somethingWentWrong'));
                        reject(error);
                    }
                };

                reader.onerror = (error) => {
                    this.toast.error(this.$t('admin.model.fileReadingError'));
                    reject(error);
                };

                reader.readAsArrayBuffer(file);
            })
        },
        // adapted to the GCS file upload
        async submitDatasetFolder() {
            // check if there is a folder first or if the folder is not empty
            if (this.selectedFiles.length === 0) {
                this.toast.error(this.$t('admin.model.noFileError'));
                return; 
            }
            if (!this.accessToken) {
                this.toast.error(this.$t('admin.model.noAccessToken'));
                return;
            }
            this.isUploading = true; // start the uploading process
            // the toast notification stays there until we terminate it when the file is uploaded and we get the confirmation from the server
            this.toast.info(this.$t('admin.model.uploadingInfo'), { timeout: false });

            try {
                const zipFile = await this.zipDataset();

                const uploadLink = await this.uploadToGCS(zipFile);

                this.toast.clear();
                this.toast.info(this.$t('admin.model.datasetUploadedTo') + uploadLink)
                this.toast.success(this.$t('admin.model.successfullyUploaded') + zipFile.name +  this.$t('admin.model.filesToGCS'));

                // reset the variable because otherwise the file names and size will linger on even after upload
                this.isUploading = false;
                this.selectedFiles = [];
                this.fileName = '';
                this.fileSize = 0;
                this.$refs.fileInput.value = ''; // clears the file selection element
                

            } catch (error) {
                this.toast.clear();
                this.toast.error(this.$t('admin.model.uploadError'));

                // debug print for us
                console.error('Dataset uplaod error: ', error.message);

                this.isUploading = false;
            }
        },
    }
}
</script>