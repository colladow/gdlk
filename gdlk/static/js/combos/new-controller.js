(function(window, angular) {
  'use strict';

  var combos = angular.module('gdlk.combos');

  combos.controller('NewController', function($scope, Commands) {
    $scope.combo = {};

    Commands.then(function(commands) {
      $scope.commands = commands;
    });
  });
})(window, window.angular);
