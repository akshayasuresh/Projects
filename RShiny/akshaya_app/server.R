library(shiny)
library(tidyverse)
#library(datasets)
#library(ggplot2)

#Define Server Logic required to plot various variables against mpg
shinyServer(function(input, output) {
  formulaText <- reactive({
   input$metric
  }) 
  #Return the formula text for printing as a caption
  output$caption <- renderText({
    formulaText()
  })
  
  #Generate a plot of the requested variable against mpg and only 
    #include outliers if requested
  output$meanPlot <- renderPlot({
    #scatterPlot(subset(metrics_by_year, metrics_by_year$TAX_YR==input$year),metrics_by_year$EMP_TYPE,formulaText)
    just_year <- subset(metrics_by_year, metrics_by_year$TAX_YR==input$year)
    y_data <- switch(input$metric,
                     "Cycle Days" = just_year$CYCDAYS,
                     "Total Exam Time" = just_year$TOT_EXTM,
                     "Total Dollar Amount" = just_year$T37_AMT,
                     "Total Count" = just_year$total_count)
    x_data <- switch(input$category,
                     "RA vs. TCO" = just_year$EMP_TYPE,
                     "Diff vs Non.Diff Selected" = just_year$DIF_FLAG)
    ggplot(just_year,
           aes(x=factor(x_data), y=y_data, color=factor(x_data), fill=factor(x_data))) + stat_summary(fun.y="mean", geom="bar")
  })
  
  output$timePlot <- renderPlot({
    y_data <- switch(input$metric,
                     "Cycle Days" = metrics_by_year$CYCDAYS,
                     "Total Exam Time" = metrics_by_year$TOT_EXTM,
                     "Total Dollar Amount" = metrics_by_year$T37_AMT,
                     "Total Count" = metrics_by_year$total_count)
    x_data <- switch(input$category,
                     "RA vs. TCO" = metrics_by_year$EMP_TYPE,
                     "Diff vs Non.Diff Selected" = metrics_by_year$DIF_FLAG)
    ggplot(metrics_by_year,
           aes(x=metrics_by_year$TAX_YR, y=y_data, color=factor(x_data), fill=factor(x_data))) + stat_summary(fun.y="mean", geom="line")
  })
  
  output$table <- renderTable({
    subset(metrics_by_year, metrics_by_year$TAX_YR==input$year)
  })
  
  output$summaryText <- renderText({
    "While DIF scores are useful, we cannot discount the use of traditional methods."
  })
})