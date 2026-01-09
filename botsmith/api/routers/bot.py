from fastapi import APIRouter, Depends, HTTPException
from botsmith.api.schemas import CreateBotRequest, BotResponse, GenericResponse
from botsmith.api.deps import get_botsmith_app
from botsmith.app import BotSmithApp

router = APIRouter()

@router.post("/create", response_model=BotResponse)
def create_bot(
    request: CreateBotRequest,
    app: BotSmithApp = Depends(get_botsmith_app)
):
    try:
        project_name = request.project_name or "api_generated_bot"
        # Sanitize project name to ensure filesystem compatibility (especially for Windows)
        # and Python package naming conventions (lowercase, underscores).
        project_name = project_name.strip().lower().replace(" ", "_")

        result = app.create_bot(request.prompt, project_name)
        
        # Extract relevant info for response
        res_data = result.get("result", {})
        context = res_data.get("context", {})
        workflow_def = result.get("workflow", {})
        
        generated_files = []
        if "generated_files" in context:
            generated_files = context["generated_files"]
        elif "files" in res_data:
             generated_files = res_data["files"]

        return BotResponse(
            status="success",
            message=f"Bot '{project_name}' created successfully",
            workflow_name=workflow_def.get("workflow_name", "unknown"),
            steps_executed=len(context.get("executed_steps", [])), # Ideally we track this better
            generated_files=generated_files,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{project_name}")
async def download_bot(project_name: str, app: BotSmithApp = Depends(get_botsmith_app)):
    """
    Download the generated bot as a ZIP file.
    """
    from botsmith.api.utils.archiver import zip_project
    from botsmith.utils.filesystem import LocalFileSystem
    from pathlib import Path
    
    # Locate project - align with WorkflowExecutor logic
    norm_project_name = project_name.lower().replace(" ", "_")
    
    # Executor uses 'generated' output
    project_path = Path("generated") / norm_project_name
    
    if not project_path.exists():
        return Response(content="Project not found", status_code=404)
        
    zip_io = zip_project(project_path)
    
    return Response(
        content=zip_io.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={project_name}.zip"
        }
    )

