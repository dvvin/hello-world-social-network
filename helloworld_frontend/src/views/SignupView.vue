<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin>
        <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c&display=swap" rel="stylesheet">
    </head>

    <body class>
        <div class="lg:flex">
            <div class="font-m-plus-rounded-1c lg:w-1/2 h-[740px] rounded-l-xl bg-white xl:max-w-screen-sm">
                <div class="mt-10 px-12 sm:px-24 md:px-48 lg:px-12 lg:mt-16 xl:px-24 xl:max-w-2xl">
                    <h2 class="text-center text-4xl text-emerald-500 font-display font-semibold lg:text-left xl:text-5xl
                    xl:text-bold">
                        Join helloworld!
                    </h2>

                    <div class="mt-12">
                        <form>
                            <div>
                                <div class="text-sm font-bold text-gray-700 tracking-wide">
                                    Email Address
                                </div>
                                <input
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="" placeholder="Email">
                            </div>

                            <div class="mt-8">
                                <div class="flex justify-between items-center">
                                    <div class="text-sm font-bold text-gray-700 tracking-wide">
                                        Username
                                    </div>
                                    <!-- <div>
                                        <a class="text-xs font-display font-semibold text-emerald-600 hover:text-emerald-700
                                        cursor-pointer">
                                            Forgot Password?
                                        </a>
                                    </div> -->
                                </div>
                                <input
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="" placeholder="Username">

                            </div>
                            <div class="mt-8">
                                <div class="flex justify-between items-center">
                                    <div class="text-sm font-bold text-gray-700 tracking-wide">
                                        Password
                                    </div>
                                </div>
                                <input
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="" placeholder="Password">

                            </div>
                            <div class="mt-8">
                                <div class="flex justify-between items-center">
                                    <div class="text-sm font-bold text-gray-700 tracking-wide">
                                        Re-enter Password
                                    </div>
                                </div>
                                <input
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="" placeholder="Password">

                            </div>
                            <div class="mt-10">
                                <button class="bg-emerald-500 text-gray-100 p-4 w-full rounded-full tracking-wide
                                font-semibold font-display focus:outline-none focus:shadow-outline hover:bg-emerald-600
                                shadow-lg">
                                    Sign Up
                                </button>
                            </div>
                        </form>
                        <div class="mt-12 text-sm font-display font-semibold text-gray-700 text-center">
                            Already have an account?
                            <RouterLink :to="{ name: 'login' }" class="cursor-pointer text-emerald-600 hover:text-emerald-800">
                                Log In!
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>

            <div class="rounded-r-xl hidden lg:flex bg-purple-100 items-center justify-center flex-1 ">
                <div class="">
                    <div>
                        <img src="/hw_logo_trans.png" alt="Logo" class="rounded-r-xl h-[740px]">
                    </div>
                </div>
            </div>
        </div>


    </body>
</template>
