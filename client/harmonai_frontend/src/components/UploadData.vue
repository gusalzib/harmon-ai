<template>
    <div class="upload-data-section" id="upload" v-if="activeSection === 'dataUpload'">
        <h3>{{ $t('admin.model.uploadData') }}</h3>

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
import { useToast } from 'vue-toastification'

export default {
    name: 'UploadData',
    data() {
        return {

            url: 'http://localhost:8000/users/admin-upload',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000,
            activeSection: 'dataUpload', //this controls which section in visible to the user at any time.
            // selectedFile: null,
            fileName: '', 
            fileSize: 0,
            isUploading: false, // monitors whether the file upload is ongoing

            // experimental code: accepting an entire folder instead of a single csv file
            selectedFiles: [], // an array that saves selected files 


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable

    },
    methods: {
        // handleFileSubmit() {
        //     // we store the file object from the upload event 
        //     const file = event.target.files[0]

        //     // make sure the file typs is strictly csv
        //     if (file && file.type === 'text/csv' || file.name.endsWith('.csv')) {
        //         this.selectedFile = file;
        //         this.fileName = file.name; 

        //         // size is divided by 1024 because we get it in bytes and we want it in MB
        //         this.fileSize = file.size/1024;
        //     } else {
        //         this.selectedFile = null;
        //         this.fileName = '';
        //         this.toast.error(this.$t('admin.model.fileTypeError'));

        //         // clear the file selection 
        //         this.$refs.fileInput.value = '';
        //     }
        // },
        // async submitDataset() {
        //     // check if there is a file first 
        //     if (!this.selectedFile) {
        //         this.toast.error(this.$t('admin.model.noFileError'));
        //         return; 
        //     }

        //     this.isUploading = true; // start the uploading process

        //     // declare a form data object and add the uploaded file to it 
        //     const formData = new FormData();
        //     formData.append('datasetFile', this.selectedFile);

        //     // the toast notification stays there until we terminate it when the file is uploaded and we get the confirmation from the server
        //     this.toast.info(this.$t('admin.model.uploadingInfo'), { timeout: false });

        //     try {
        //         const response = await axios.post(`${this.url}`, formData, {
        //             withCredentials: true,
        //             headers: {
        //                 "X-CSRFToken": getCsrfToken()
        //             }
        //         });

                
        //         // if we get a confirmation from the server
        //         // we remove the processing toast and we proceed to notify the admin the file is uploaded successfully
        //         if (response.status === 200) {
        //             this.toast.clear();
        //             this.toast.success(this.$t('admin.model.uploadSuccessful'));

        //             // clearing the form of any left over data
        //             this.selectedFile = null;
        //             this.fileName = '';
        //             this.$refs.fileInput.value = '';
        //             this.isUploading = false;
        //         }

        //     } catch (error) {
        //         this.toast.clear();
        //         this.toast.error(this.$t('admin.model.uploadError'));

        //         // debug print for us
        //         console.error('Dataset uplaod error: ', error.message);

        //         this.isUploading = false;
        //     }
        // },
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

            for (let index = 0; index < files.length; index++) {
                const file = files[index];
                    this.selectedFiles.push(file);
                    totalSize = totalSize + file.size
            }

            this.fileName = `${this.selectedFiles.length} files selected`
            // we divide by 1024 squared because we are converting from bytes to kilobytes and then from kilobytes to megabytes
            this.fileSize = totalSize / (1024 * 1024);
            this.toast.info(`Folder selected: ${this.selectedFiles.length} files (${this.fileSize.toFixed(2)} MB)`)


        },
        async submitDatasetFolder() {
            // check if there is a folder first or if the folder is not empty
            if (this.selectedFiles.length === 0) {
                this.toast.error(this.$t('admin.model.noFileError'));
                return; 
            }

            this.isUploading = true; // start the uploading process

            // declare a form data object and add the uploaded file to it 
            const formData = new FormData();
            this.selectedFiles.forEach(file => {
                // this file.webkitRelativePath will add the file path withing the selected folder to maintin the structure of the folder we are uploading 
                formData.append('datasetFile', file, file.webkitRelativePath)
            })

            // the toast notification stays there until we terminate it when the file is uploaded and we get the confirmation from the server
            this.toast.info(this.$t('admin.model.uploadingInfo'), { timeout: false });

            try {
                const response = await axios.post(`${this.url}`, formData, {
                    withCredentials: true,
                    headers: {
                        "X-CSRFToken": getCsrfToken()
                    }
                });
                console.log('Dataset Folder Upload Response: ', response)
                // if we get a confirmation from the server
                // we remove the processing toast and we proceed to notify the admin the file is uploaded successfully
                if (response.status === 200) {
                    this.toast.clear();
                    this.toast.success(this.$t('admin.model.uploadSuccessful'));

                    // clearing the form of any left over data
                    this.selectedFile = null;
                    this.fileName = '';
                    this.$refs.fileInput.value = '';
                    this.isUploading = false;
                }

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