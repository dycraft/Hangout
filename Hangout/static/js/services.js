(function () {
  'use strict';

  angular
    .module('hangout.services', ['ngCookies'])
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Authentication($cookies, $http) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Authentication = {
      getAuthenticatedAccount: getAuthenticatedAccount,
      isAuthenticated: isAuthenticated,
      login: login,
      register: register,
      setAuthenticatedAccount: setAuthenticatedAccount,
      unauthenticate: unauthenticate
    };
    return Authentication;

    function register(email, password, username) {
      return $http.post('/api/register', {
        name: username,
        password: password,
        email: email,
      });
    }

    function login(email, password) {
      return $http.post('/api/login', $.param({
        email: email, 
        password: password,
      })).then(loginSuccessFn, loginErrorFn);
        
      function loginSuccessFn(data, status, headers, config) {
        console.log(data.data);
        Authentication.setAuthenticatedAccount(data.data);
        window.location = '/';
      }

      function loginErrorFn(data, status, headers, config) {
        console.log(data.data);
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
