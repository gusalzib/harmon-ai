<template>

    <div class="login-form-container">
        <div class="login-form">
            <label for="login_email"> {{ $t('labels.email') }} </label>
            <input id="login_email" class="login_input" type="email" placeholder="email">
            <br>
            <label for="login_password"> {{ $t('labels.password') }} </label>
            <input id="login_password" class="login_input" type="password" placeholder="password">
            <button type="submit"> {{ $t('buttons.login') }} </button>
        </div>
    </div>
</template>

<script>

</script>