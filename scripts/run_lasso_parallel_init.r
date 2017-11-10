args <- commandArgs(trailingOnly = TRUE)
targetExpressionFile <- toString(args[1])
regulatorExpressionFile <- toString(args[2])
allowedMatrixFile <- toString(args[3])
perturbationMatrixFile <- toString(args[4])
lassoAdjMtrFileName <- toString(args[5])
outputDirectory <- toString(args[6])
microarrayFlag <- 1

source("run_lasso_parallel.r")
library(Rmpi)
mpi.bcast.Robj2slave(targetExpressionFile)
mpi.bcast.Robj2slave(regulatorExpressionFile)
mpi.bcast.Robj2slave(allowedMatrixFile)
mpi.bcast.Robj2slave(perturbationMatrixFile)
mpi.bcast.Robj2slave(microarrayFlag)
mpi.bcast.Robj2slave(outputDirectory)

mpi.remote.exec(source("run_lasso_parallel_single_process.r"))
mpi.remote.exec(reportid())
uniform.solution <- lars.multi.optimize.parallel()

lasso_component <- uniform.solution[[1]]
write.table(lasso_component,file.path(outputDirectory,lassoAdjMtrFileName),row.names=FALSE,col.names=FALSE,quote=FALSE)
#save(solution,file="solution")
