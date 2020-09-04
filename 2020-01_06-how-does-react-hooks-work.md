---
layout: post
title: How does react-hooks work?
date: 2020-01-31 10:18:00
tags: technology
---

SOURCE:

- [https://reactjs.org/docs/hooks-intro.html](https://reactjs.org/docs/hooks-intro.html)
- [https://www.youtube.com/watch?v=dpw9EHDh2bM&feature=emb_logo](https://www.youtube.com/watch?v=dpw9EHDh2bM&feature=emb_logo)
- [https://medium.com/@morgler/dont-use-redux-9e23b5381291](https://medium.com/@morgler/dont-use-redux-9e23b5381291)
- [https://www.newline.co/@CarlMungazi/a-journey-through-the-usestate-hook--a4983397](https://www.newline.co/@CarlMungazi/a-journey-through-the-usestate-hook--a4983397)

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/reactlifecycle.png)</span>

Why react-hooks?

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/reacthooks.png)</span>

```javascript
const ComponentWithHook = () => {
  const [count, setCount] = React.useState(0);

  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
};

ReactDOM.render(<ComponentWithHook />, document.getElementById("root"));
```

Hooks were created to encapsulate side effects and stateful behaviour in such components. If we look at this code through our data structure lens, we can see that:

ComponentWithHook is a function which returns an object (all JXS calls are translated into objects by this babel plugin)

In ComponentWithHook, we call a function that returns two values which we destructure

React hooks has been created to avoid developers introducing too much abstraction with a separate state management library (redux, mobx...). That often requires to jumb between different files, write excessive amounts of code and lose time.

The Hooks are stored as a linked list. What’s a linked list? There is actually a ton to linked lists, but in its most basic form a linked list is a data structure that consists of nodes. Each node has its data and also a reference that points to the next node in the list. The order of nodes is entirely dependent on each node’s reference to the next.

On the first render of a component, a linked list of the Hooks called gets created and on subsequent renders.

In Javascript this is can look something like this:

React components pass through three lifecycles: Mounting, Updating and Unmounting.

- Mounting is simply putting a component in the DOM by converting the virtual components into actual DOM elements that are placed in the DOM by React.
- Updating is whenever there is a change in the component. This could be either via props or state.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/state.png)</span>

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/usestate.png)</span>

The idea is to create an array of listeners and only one state object. Every time that one component changes the state, all subscribed components get their setState() functions fired and get updated.

We can do that by calling useState() inside our custom Hook. But, instead returning the setState() function, we add it to an array of listeners and return a function which updates the state object and run all listeners functions.

- The state of a component is an object that holds information that may change over the lifetime of the component.
- Unmounting is when a component is removed from the DOM

With functional components, some of these lifecycle methods are mimicked with react hooks. React Hooks are a way for your function components to “hook” into React’s lifecycle and state.

```javascript
let hooks = null;

export function useHook() {
  hooks.push(hookData);
}

function reactInternalRenderAComponentMethod(component) {
  hooks = [];
  component();
  let hooksForThisComponent = hooks;
  hooks = null;
}
```

I’d say Hooks are about as much magic as calling array.push and array.pop (for which the call order matters too!).

```javascript
const MyReact = (function () {
  let hooks = [];
  let currentHook = 0; // array of hooks, and an iterator!
  return {
    render(Component) {
      const Comp = Component(); // run effects
      Comp.render();
      currentHook = 0; // reset for next render
      return Comp;
    },
    useEffect(callback, depArray) {
      const hasNoDeps = !depArray;
      const deps = hooks[currentHook]; // type: array | undefined
      const hasChangedDeps = deps
        ? !depArray.every((el, i) => el === deps[i])
        : true;
      if (hasNoDeps || hasChangedDeps) {
        callback();
        hooks[currentHook] = depArray;
      }
      currentHook++; // done with this hook
    },
    useState(initialValue) {
      hooks[currentHook] = hooks[currentHook] || initialValue; // type: any
      const setStateHookIndex = currentHook; // for setState's closure!
      const setState = (newState) => (hooks[setStateHookIndex] = newState);
      return [hooks[currentHook++], setState];
    },
  };
})();
```

```javascript
// Example 0
function useState(initialValue) {
  var _val = initialValue; // _val is a local variable created by useState
  function state() {
    // state is an inner function, a closure
    return _val; // state() uses _val, declared by parent funciton
  }
  function setState(newVal) {
    // same
    _val = newVal; // setting _val without exposing _val
  }
  return [state, setState]; // exposing functions for external use
}
var [foo, setFoo] = useState(0); // using array destructuring
console.log(foo()); // logs 0 - the initialValue we gave
setFoo(1); // sets _val inside useState's scope
console.log(foo()); // logs 1 - new initialValue, despite exact same call
```

⚡️ Effect Hook

You’ve likely performed data fetching, subscriptions, or manually changing the DOM from React components before. We call these operations “side effects” (or “effects” for short) because they can affect other components and can’t be done during rendering.

Instead of thinking in terms of “mounting” and “updating”, you might find it easier to think that effects happen “after render”. React guarantees the DOM has been updated by the time it runs the effects. When React renders our component, it will remember the effect we used, and then run our effect after updating the DOM.

Unlike componentDidMount or componentDidUpdate, effects scheduled with useEffect don’t block the browser from updating the screen. By default, effects run after every completed render. But, you can choose to fire it only when certain values have changed, passing an array of variables as a second optional parameter.

This makes your app feel more responsive. The majority of effects don’t need to happen synchronously. In the uncommon cases where they do (such as measuring the layout), there is a separate useLayoutEffect Hook with an API identical to useEffect.

If you want to run an effect and clean it up only once (on mount and unmount), you can pass an empty array ([]) as a second argument. This tells React that your effect doesn’t depend on any values from props or state, so it never needs to re-run.

Often, effects create resources that need to be cleaned up before the component leaves the screen, such as a subscription or timer ID. To do this, the function passed to useEffect may return a clean-up function.
