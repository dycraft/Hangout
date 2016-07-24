(function () {
  'use strict';

  var CONST = {
        WEEK: ['SUN','MON','TUE','WED','THU','FRI','SAT'],
        TIME_SEG: ['0:00-7:00', '7:00-12:00', '12:00-18:00', '18:00-24:00']
    };

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
      vm.tags = "student";
      vm.register = register;
      function register() {
<<<<<<< HEAD
        Authentication.register(vm.email, vm.password, vm.username, getFixTime(), $('#register__tags').val(), vm.cellphone, vm.intro);
=======
        Authentication.register(vm.email, vm.password, vm.username, encodeFixedTime(), $('#register__tags').val());
>>>>>>> 1e36592d76fd3840739049c57a364d8939b28213
      }
      activate();
      function activate() {
        if (Authentication.isAuthenticated()) {
          $location.url('/');
        }
      }

      //FixedTimeTable
        vm.week = CONST.WEEK;
        vm.times = CONST.TIME_SEG;
        $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
            var tds = $('#register__fixed').find('td');
            tds.click(function () {
                onSelectTime(tds.index($(this)));
            });
        });

        //js-lib: tagsinput
        $.getScript('/static/lib/bootstrap-tagsinput/bootstrap-tagsinput.js');
    }])
    .controller('profileCtrl', ['$scope', '$location', 'Authentication', '$http', function($scope, $location, Authentication, $http){
      console.log('profile');
      var vm = this;
      vm.update_profile = update_profile;
      if (Authentication.isAuthenticated()) {
        vm.email = Authentication.getAuthenticatedAccount().user_info.email;
        vm.password = Authentication.getAuthenticatedAccount().user_info.password;
        vm.username = Authentication.getAuthenticatedAccount().user_info.name;
        vm.fix_times = Authentication.getAuthenticatedAccount().user_info.fix_times;
        vm.tags = Authentication.getAuthenticatedAccount().user_info.tags;
        vm.cellphone = Authentication.getAuthenticatedAccount().user_info.cellphone;
        vm.intro = Authentication.getAuthenticatedAccount().user_info.intro;
      }
      else {
        $location.url('/login');
      }
      function update_profile() {
<<<<<<< HEAD
        Authentication.update_profile(vm.email, vm.password, vm.username, getFixTime(), $('#profile__tags').val(), vm.cellphone, vm.intro);
=======
        Authentication.update_profile(vm.email, vm.password, vm.username, encodeFixedTime(), $('#profile__tags').val());
>>>>>>> 1e36592d76fd3840739049c57a364d8939b28213
      }

      //FixedTimeTable
        vm.week = CONST.WEEK;
        vm.times = CONST.TIME_SEG;
        $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
            var tds = $('#register__fixed').find('td');
            tds.click(function () {
                onSelectTime(tds.index($(this)));
            });
            decodeFixedTime(vm.fix_times);
        });

        //js-lib: tagsinput
        $.getScript('/static/lib/bootstrap-tagsinput/bootstrap-tagsinput.js');
    }])
    .controller('activityCtrl', ['$location', '$scope', 'Authentication', function($location, $scope, Authentication){
      $(".act-nav").click(function(){
        $(".act-nav").not(this).removeClass("active");
        $(this).addClass("active");
      })
      $scope.myActs = function() {
        $scope.page_title = "组织的活动";
        $scope.act_type = "my_act";
      }
      $scope.joinActs = function() {
        $scope.page_title = "参与的活动";
        $scope.act_type = "part_act";
      }
      $scope.orgActs = function() {
        $scope.page_title = "组织活动";
        $scope.act_type = "apply_act";
      }
      $scope.otherActs = function() {
        $scope.page_title = "随便逛逛";
        $scope.act_type = "recommend_act";
      }
      $scope.myActs();
    }])
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
      $scope.activity = function() {
        $location.url('/activity');
      }
      $scope.friends = function() {
        $location.url('/friends');
      }
      $scope.register = register;
      if (Authentication.isAuthenticated()) {
        $scope.displayName = Authentication.getAuthenticatedAccount().user_info.name;
        $('#nav_user').css({'display': 'block'});
        $('#nav_register').css({'display': 'none'});
        $('#nav_activity').css({'display': 'block'});
        $('#nav_friends').css({'display': 'block'});
        $scope.logger = '登出';
        $scope.login_logout = logout;
      }
      else {
        $scope.displayName = '注册';
        $('#nav_user').css({'display': 'none'});
        $('#nav_activity').css({'display': 'none'});
        $('#nav_friends').css({'display': 'none'});
        $('#nav_register').css({'display': 'block'});
        $scope.logger = '登录';
        $scope.login_logout = login;
      }
      $rootScope.$on('login_done', function(){
        $scope.displayName = Authentication.getAuthenticatedAccount().user_info.name;
        $('#nav_user').css({'display': 'block'});
        $('#nav_register').css({'display': 'none'});
        $('#nav_activity').css({'display': 'block'});
        $('#nav_friends').css({'display': 'block'});
        $scope.logger = '登出';
        $scope.login_logout = logout;
      })
      $rootScope.$on('logout_done', function(){
        $scope.displayName = '注册';
        $('#nav_user').css({'display': 'none'});
        $('#nav_activity').css({'display': 'none'});
        $('#nav_friends').css({'display': 'none'});
        $('#nav_register').css({'display': 'block'});
        $scope.logger = '登录';
        $scope.login_logout = login;
      })
    }]);

    //FixedTimeTable
    var len = 28;
    var fixedTimeArray = [];//global
    for (var i = 0; i < len; i++) {
        fixedTimeArray.push(0);
    }

    function onSelectTime(value) {
        var tds = $('#register__fixed').find('td');

        if (value >= 0 && value < len) {
            fixedTimeArray[value] = 1 - fixedTimeArray[value];
        }

        if (fixedTimeArray[value] === 1) {
            tds[value].style.backgroundColor = '#FFF';
        } else {
            tds[value].style.backgroundColor = '#EBEBEB';
        }
    }

    function encodeFixedTime() {
        var binStr = '';
        for (var i = 0; i < len; i++) {
            binStr += fixedTimeArray[i];
        }
        return parseInt(binStr, 2);
    }

    function decodeFixedTime(fixedTime) {
        var timeStr = fixedTime.toString(2);
        var s = '';
        for (var k = 0; k < len-timeStr.length; k++) {
            s += '0';
        }
        timeStr = s + timeStr;
        var strTimeArray = timeStr.split("");
        for (var i = 0; i < len; i++) {
            fixedTimeArray[i] = parseInt(strTimeArray[i]);
        }
        
        //update view
        var tds = $('#register__fixed').find('td');
        for (var j = 1; j < len; j++) {
            if (fixedTimeArray[j] === 1) {
                tds[j].style.backgroundColor = '#FFF';
            } else {
                tds[j].style.backgroundColor = '#EBEBEB';
            }
        }
    }
})();
