(function () {
  'use strict';

  angular
    .module('hangout.services', ['ngCookies'])
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http', '$rootScope', '$location'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Authentication($cookies, $http, $rootScope, $location) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Authentication = {
      getAuthenticatedAccount: getAuthenticatedAccount,
      isAuthenticated: isAuthenticated,
      login: login,
      logout: logout,
      register: register,
      setAuthenticatedAccount: setAuthenticatedAccount,
      unauthenticate: unauthenticate
    };
    return Authentication;

    function register(email, password, username, fix_times, tags) {
      return $http.post('/api/register', $.param({
        name: username,
        password: password,
        email: email,
        fix_times: fix_times,
        tags: tags,
        portrait: 'afda',
      })).then(registerSuccessFn, registerErrorFn);

      function registerSuccessFn(data, status, headers, config) {
        Authentication.login(email, password);
      }

      function registerErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

    function update_profile(email, password, username, fix_times, tags) {
      return $http.post('/api/user/update', $.param({
        name: username,
        password: password,
        email: email,
        fix_times: fix_times,
        tags: tags,
        portrait: 'afda',
      })).then(updateSuccessFn, updateErrorFn);

      function updateSuccessFn(data, status, headers, config) {
        Authentication.login(email, password);
      }

      function updateErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

    function login(email, password) {
      return $http.post('/api/login', $.param({
        email: email, 
        password: password,
      })).then(loginSuccessFn, loginErrorFn);
        
      function loginSuccessFn(data, status, headers, config) {
        Authentication.setAuthenticatedAccount(data.data);
        $rootScope.$broadcast('login_done');
        $location.url('/');
      }

      function loginErrorFn(data, status, headers, config) {
        console.log(data.data);
        console.error('Epic failure!');
      }
    }

    function logout() {
      return $http.post('/api/logout')
        .then(logoutSuccessFn, logoutErrorFn);
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();
        $rootScope.$broadcast('logout_done');
        $location.url('/');
      }
      function logoutErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

    function getAuthenticatedAccount() {
      if (!$cookies.authenticatedAccount) {
        return;
      }
      return JSON.parse($cookies.authenticatedAccount);
    }

    function isAuthenticated() {
      return !!$cookies.authenticatedAccount;
    }

    function setAuthenticatedAccount(account) {
        console.log(account);
      $cookies.authenticatedAccount = JSON.stringify(account);
    }

    function unauthenticate() {
      delete $cookies.authenticatedAccount;
    }
  }
})();
