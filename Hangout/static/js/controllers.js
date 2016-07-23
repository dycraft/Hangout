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
        if (Authentication.isAuthenticated()) {
          $location.url('/');
        }
      }
      function login() {
        Authentication.login(vm.email, vm.password);
      }
    }])
    .controller('registerCtrl', ['$scope', '$location', 'Authentication', function($scope, $location, Authentication){
      console.log('register');
      var vm = this;
      vm.placeholder = "cat dog";
      vm.register = register;
      function register() {
        Authentication.register(vm.email, vm.password, vm.username, vm.fix_times, vm.tags);
      }
      $.getScript('/static/lib/bootstrap-tagsinput/bootstrap-tagsinput.js');
    }])
    .controller('profileCtrl', ['$scope', '$location', 'Authentication', '$http'], function($scope, $location, Authentication, $http){
      console.log('profile');
      var vm = this;
      vm.update_profile = update_profile;
      function update_profile() {
        Authentication.register(vm.email, vm.password, vm.username, vm.fix_times, vm.tags);
      }
    })
    .controller('navbarCtrl', ['$location', '$scope', '$rootScope', 'Authentication', function($location, $scope, $rootScope, Authentication){
      function login() {
        $location.url('/login');
      }
      function logout() {
        Authentication.logout();
      }
      function register() {
        $location.url('/register');
      }
      $scope.register = register;
      if (Authentication.getAuthenticatedAccount()) {
        $scope.displayName = Authentication.getAuthenticatedAccount().user_info.name;
        $('#nav_user').css({'display': 'block'});
        $('#nav_register').css({'display': 'none'});
        $scope.logger = 'logout';
        $scope.login_logout = logout;
      }
      else {
        $scope.displayName = 'register';
        $('#nav_user').css({'display': 'none'});
        $('#nav_register').css({'display': 'block'});
        $scope.logger = 'login';
        $scope.login_logout = login;
      }
      $rootScope.$on('login_done', function(){
        $scope.displayName = Authentication.getAuthenticatedAccount().user_info.name;
        $('#nav_user').css({'display': 'block'});
        $('#nav_register').css({'display': 'none'});
        $scope.logger = 'logout';
        $scope.login_logout = logout;
      })
      $rootScope.$on('logout_done', function(){
        $scope.displayName = 'register';
        $('#nav_user').css({'display': 'none'});
        $('#nav_register').css({'display': 'block'});
        $scope.logger = 'login';
        $scope.login_logout = login;
      })
    }]);
})();
