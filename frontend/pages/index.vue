<template>
<div class="bg-gray-300">
  <div v-if="message" class="text-white max-w-md mx-auto py-6 rounded relative mb-4 bg-red-400 ">
      <span class="text-xl inline-block mr-5 align-middle">
          <i class="fas fa-bell" />
      </span>
      <span class="inline-block align-middle mr-8">
        <b class="capitalize">Sucess!</b> Moved to Resolved!
      </span>
      <button class="absolute bg-transparent text-2xl font-semibold leading-none right-0 top-0 mt-4 mr-6 outline-none focus:outline-none">
        <span>×</span>
      </button>
  </div>
  <div v-if="message1" class="text-white max-w-md mx-auto py-6 rounded relative mb-4 bg-green-400 ">
      <span class="text-xl inline-block mr-5 align-middle">
          <i class="fas fa-bell" />
      </span>
      <span class="inline-block align-middle mr-8">
        <b class="capitalize">Sucess!</b> Moved to Unresolved!
      </span>
      <button class="absolute bg-transparent text-2xl font-semibold leading-none right-0 top-0 mt-4 mr-6 outline-none focus:outline-none">
        <span>×</span>
      </button>
  </div>
  <div v-if="message2" class="text-white max-w-md mx-auto py-6 rounded relative mb-4 bg-blue-400 ">
      <span class="text-xl inline-block mr-5 align-middle">
          <i class="fas fa-bell" />
      </span>
      <span class="inline-block align-middle mr-8">
        <b class="capitalize">Sucess!</b> Moved to Unresolved!
      </span>
      <button class="absolute bg-transparent text-2xl font-semibold leading-none right-0 top-0 mt-4 mr-6 outline-none focus:outline-none">
        <span>×</span>
      </button>
  </div>
  <div v-if="message3" class="text-white max-w-md mx-auto py-6 rounded relative mb-4 bg-yellow-400 ">
      <span class="text-xl inline-block mr-5 align-middle">
          <i class="fas fa-bell" />
      </span>
      <span class="inline-block align-middle mr-8">
        <b class="capitalize">Sucess!</b> Undo Operation Done!
      </span>
      <button class="absolute bg-transparent text-2xl font-semibold leading-none right-0 top-0 mt-4 mr-6 outline-none focus:outline-none">
        <span>×</span>
      </button>
  </div>
    <button @click="undo(); created3()"  class="place-items-start text-black-700 font-bold py-2 px-6 bg-yellow-400 hover:bg-red-700  ">Undo</button>        
  <div class="min-h-screen flex justify-center w-54 bg-gray-300  ">
    <div>
      <div class="text-center font-semibold ">
        <h1 class="text-3xl text-center">
          <span class="text-blue-700 tracking-wide">Unresolved </span>
        </h1>  
      </div>
    
      <div v-for="(error, index) in unresolved" :key="error.index" class="bg-red-400 "  >
        <ul class=" list-reset flex flex-col " >
	        <li class=" rounded-t relative -mb-px block border p-4 border-grey   ">`{{ error.code }}` - {{ error.text }}
            <div class="mt-8 flex justify-center ">
              <div class="inline-flex rounded-md bg-white shadow group border-indigo-500 hover:bg-white hover:shadow-lg hover:border-transparent">
                <button @click="pushToResolve(error, index); created() "  class="text-red-500 font-bold py-2 px-6 hover:bg-red-200">
                    Press to Resolve
                </button>
              </div>
            </div>
          </li>
	      </ul>
      </div>
    </div>
    
    <div>
      <div class="text-center font-semibold">
        <h1 class="text-3xl text-center" >
          <span class="text-blue-700 tracking-wide">Resolved </span>    
        </h1>   
      </div>
     
      <div v-for="(error, index) in resolved" :key="error.index" class="bg-green-400" >
        <ul class=" list-reset flex flex-col" >
	        <li class=" rounded-t relative -mb-px block border p-4 border-grey">`{{ error.code }}` - {{ error.text }} 
            <div class="mt-8 flex justify-center">
              <div class="inline-flex rounded-md bg-white shadow group border-indigo-500 hover:bg-white hover:shadow-lg hover:border-transparent">
                <button @click="pushToUnresolve(error, index); created1()"  class="text-green-500 font-bold py-2 px-6 hover:bg-green-200">
                    Press to Unresolve
                </button>
              </div>
            </div>
          </li>
	      </ul>
      </div>
    </div>
    

    <div >
      <div class="text-center font-semibold">
        <h1 class="text-3xl text-center">
          <span class="text-blue-700 tracking-wide">Backlog </span>
        </h1>
      </div>

      <div v-for="(errors, index) in backlog" :key="errors.index" class="bg-blue-400 ">
        <ul class="list-reset flex flex-col" >
	        <li class=" rounded-t relative -mb-px block border p-4 border-grey">`{{ errors.code }}` - {{ errors.text }}
            <div class="mt-8 flex justify-center">
              <div class="inline-flex rounded-md bg-white shadow group border-indigo-500 hover:bg-white hover:shadow-lg hover:border-transparent">
                <button @click="pushToUnresolveFromBacklog(errors, index); created2()"  class="text-blue-500 font-bold py-2 px-6 hover:bg-blue-200">
                    Press to Unresolve
                </button>
              </div>
            </div>
          </li>
	      </ul>
      </div>

    </div>

  </div>
  
</div>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    try {
      const { resolved, unresolved, backlog } = await $axios.$get(
        "http://localhost:8000/get_lists"
      );
      return {
        resolved,
        unresolved,
        backlog,
        message: false,
        message1: false,
        message2: false,
        message3: false
      };
    } catch (error) {
      console.log(
        `Couldn't get error lists:\n${error}\nDid you start the API?`
      );
      console.log(
        "HINT: You can comment out the full `asyncData` method and work with mocked data for UI/UX development, if you want to."
      );
    }
  },
  data() {
    return {
      resolved: [],
      unresolved: [],
      backlog: [],
      lastAction: [],
      origin: ""
    };
  },
  methods: {
    pushToResolve:  function(error, index) {
      this.unresolved.splice(index, 1);
      this.resolved.push(error);
      this.lastAction = [];
      this.lastAction.push(error);
      this.origin = "unresolve";
      this.message = true;
      
      
      
    },

    pushToUnresolve:  function(error, index) {
      this.resolved.splice(index, 1);
      this.unresolved.push(error);
      this.lastAction = [];
      this.lastAction.push(error);
      this.origin = "resolve";
      this.message1 = true;
    },

    pushToUnresolveFromBacklog:  function(error, index) {
      this.backlog.splice(index, 1);
      this.unresolved.push(error);
      this.lastAction = [];
      this.lastAction.push(error);
      
      this.origin = "backlog";
      this.message2 = true;
    },

    undo:  function() {
      console.log(this.lastAction);
      if(this.lastAction === undefined || this.lastAction.length == 0) {
        return;
      }

      this.message3 = true;
      if(this.origin == "unresolve") {
        this.unresolved.push(this.lastAction[0]);
        this.resolved.splice(this.resolved.length - 1, 1);
        this.lastAction = [];
      }
      if(this.origin == "resolve") {
        this.resolved.push(this.lastAction[0]);
        this.unresolved.splice(this.unresolved.length - 1, 1);
        this.lastAction = [];
      }
      if(this.origin == "backlog") {
        this.backlog.push(this.lastAction[0]);
        this.unresolved.splice(this.unresolved.length - 1, 1);
        this.lastAction = [];
      }
      
      console.log(this.unresolved.length);
      console.log(this.resolved.length);
      console.log(this.backlog.length);
      
    },
  created() {
    setTimeout(() => {
      this.message = false
    }, 2000)
  },
  created1() {
    setTimeout(() => {
      this.message1 = false
    }, 2000)
  },
  created2() {
    setTimeout(() => {
      this.message2 = false
    }, 2000)
  },
  created3() {
    setTimeout(() => {
      this.message3 = false
    }, 2000)
  }  
  }
};
</script>
