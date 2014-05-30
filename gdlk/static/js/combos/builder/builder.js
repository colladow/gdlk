(function(window, angular) {
  'use strict';

  var builder = angular.module('gdlk.combos.builder', ['gdlk.utils']);

  builder.directive('builder', function(Commands, typeOrder) {
    var link = function(scope, element, attrs) {
      var counter = 0;

      scope.types = {};
      scope.typeOrder = typeOrder;

      // fill in "ids" for the current set of commands
      // if there are any
      angular.forEach(scope.commands, function(command) {
        command.id = counter;
        counter += 1;
      });

      // fetch the full list of commands from the server
      Commands.then(function(commands) {
        angular.forEach(commands, function(command) {
          var type = scope.types[command.type];

          if (typeof type === 'undefined') {
            scope.types[command.type] = [];
          }

          // shove them in the types map, wanna keep the
          // different command types separate for now
          scope.types[command.type].push(command);
        });
      });

      scope.addCommand = function(command) {
        var copy = angular.copy(command);

        copy.id = counter;
        scope.commands.push(copy);
        counter += 1;
      };

      scope.removeCommand = function(command) {
        var index = -1;

        angular.forEach(scope.commands, function(cmd, i) {
          if (command.id === cmd.id) {
            index = i;
            return;
          }
        });

        if (index === -1) return;

        scope.commands.splice(index, 1);
      };
    };

    return {
      restrict: 'E',
      scope: {
        commands: '=commands'
      },
      templateUrl: '/static/js/combos/builder/builder.html',
      link: link
    };
  });

})(window, window.angular);
