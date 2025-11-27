<template>

    <div class="signup-form-container">
        <div class="signup-form">
            <label for="signup_email">  {{ $t('labels.username') }}  </label>
            <input id="signup_username" class="signup_input" type="text" placeholder="username">
            <label for="signup_email">  {{ $t('labels.email') }}  </label>
            <input id="signup_email" class="signup_input" type="email" placeholder="email">
            <label for="signup_password">  {{ $t('labels.password') }}  </label>
            <input id="signup_password" class="signup_input" type="password" placeholder="password">
            <button type="submit"> {{ $t('buttons.signupBtn') }} </button>
        </div>
    </div>
</template>

<script>

</script>