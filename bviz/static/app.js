// Author : Jeeyoung Kim
// Utility code, formatted under its own function
// space.
var bviz = bviz || {}; // namespace.

(function($){
  /** Load a given tempplate, using the selector. */
  $.fn.compile = function() {
    var txt = this.contents()[0].data;
    var tmpl = _.template(txt);
    return tmpl;
  };
})(jQuery);

// makeClass - By John Resig (MIT Licensed)
// Referende: http://ejohn.org/blog/simple-class-instantiation/
function makeClass(){
  return function(args){
    if ( this instanceof arguments.callee ) {
      if ( typeof this.init == "function" )
        this.init.apply( this, args.callee ? args : arguments );
    } else
      return new arguments.callee( arguments );
  };
};

assert = function(exp, message) {
  /** Assertions */
  AssertException = makeClass();
  AssertException.prototype.init = function(message) { this.message = message; };
  AssertException.prototype.toString = function () {
    return 'AssertException: ' + this.message;
  };
  if (!exp) {
    console.log("Assertion failed", message);
    throw new AssertException(message);
  }
};
