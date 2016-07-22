(function () {
  'use strict';

  angular.module('hangout.controllers', [])
    .controller('homepageCtrl', ['$scope', '$location', function($scope, $location){
      console.log('homepage');
      $scope.login = function(){
        $location.url('/login');
      }
    }])
    .controller('loginCtrl', ['$scope', '$location', 'Authentication', function($scope, $location, Authentication){
      console.log('login');
      var vm = this;
      vm.login = login;
      activate();
      function activate() {
        // If the user is authenticated, they should not be here.
        if (Authentication.isAuthenticated()) {
          $location.url('/');
        }
      }
      function login() {
        Authentication.login(vm.email, vm.password);
      }
    }])
    .controller('navbarCtrl', ['$scope', '$rootScope', 'Authentication', function($scope, $rootScope, Authentication){
      $scope.displayName = Authentication.getAuthenticatedAccount()['name'];
      $rootScope.$on('login_done', function(){
        $scope.displayName = Authentication.getAuthenticatedAccount()['name'];
      })
    }]);
})();