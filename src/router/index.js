import {createRouter, createWebHistory} from "vue-router";

import WorkspaceView from "./views/workspace/workspace.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/workspace",
            component: WorkspaceView,
        },
    ]
});

export default router;