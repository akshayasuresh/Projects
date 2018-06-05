library(shiny)

# Define UI for application
shinyUI(pageWithSidebar(
  
  #Application title
  headerPanel("Time Sheet Distribution"),
  
  sidebarPanel(
    selectInput("metric", label="Metric:",
                choices = c("Cycle Days",
                            "Total Exam Time",
                            "Total Dollar Amount",
                            "Total Count")),
    
    selectInput("category", label="Category:",
                choices = c("RA vs. TCO",
                            "Diff vs Non.Diff Selected")),
    
    #checkboxInput("outliers", "Include Outliers?", FALSE),
    
    sliderInput("year", "Fiscal Year:", 2010, 2012, 2010, step = 1,
                animate=animationOptions(interval=1000, loop=T))
    
  ),
  
  mainPanel(
    h3(textOutput("caption")),
    tabsetPanel(
      tabPanel("Category Plot", plotOutput("meanPlot")),
      tabPanel("Time Plot", plotOutput("timePlot")),
      tabPanel("Table", tableOutput("table")),
      tabPanel("Summary", verbatimTextOutput("summaryText"))
    )
  )
  
))