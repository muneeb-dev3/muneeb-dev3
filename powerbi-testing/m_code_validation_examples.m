// M Code Validation Examples for Power BI
// These queries can be added to your Power BI project to validate transformations

// ============================================================
// 1. ROW COUNT VALIDATION
// ============================================================
// Compare row count between source and transformed table
let
    SourceTable = #"Your Source Table",
    TransformedTable = #"Your Transformed Table",
    SourceCount = Table.RowCount(SourceTable),
    TransformedCount = Table.RowCount(TransformedTable),
    Difference = TransformedCount - SourceCount,
    ValidationMessage = if SourceCount = TransformedCount 
                        then "✅ PASS: Row counts match (" & Number.ToText(SourceCount) & " rows)"
                        else "❌ FAIL: Row count mismatch (Source: " & Number.ToText(SourceCount) & ", Transformed: " & Number.ToText(TransformedCount) & ", Diff: " & Number.ToText(Difference) & ")",
    Result = #table(
        {"Test", "Status", "SourceRows", "TransformedRows", "Difference"},
        {{"Row Count Validation", ValidationMessage, SourceCount, TransformedCount, Difference}}
    )
in
    Result


// ============================================================
// 2. COLUMN VALIDATION
// ============================================================
// Verify expected columns exist in transformed table
let
    TransformedTable = #"Your Transformed Table",
    ExpectedColumns = {"CustomerID", "CustomerName", "OrderDate", "TotalAmount"},
    ActualColumns = Table.ColumnNames(TransformedTable),
    MissingColumns = List.RemoveItems(ExpectedColumns, ActualColumns),
    ExtraColumns = List.RemoveItems(ActualColumns, ExpectedColumns),
    ValidationStatus = if List.Count(MissingColumns) = 0 
                       then "✅ PASS: All expected columns present"
                       else "❌ FAIL: Missing columns: " & Text.Combine(MissingColumns, ", "),
    Result = #table(
        {"Test", "Status", "MissingColumns", "ExtraColumns"},
        {{"Column Validation", ValidationStatus, Text.Combine(MissingColumns, ", "), Text.Combine(ExtraColumns, ", ")}}
    )
in
    Result


// ============================================================
// 3. NULL VALUE CHECK
// ============================================================
// Count null values in critical columns
let
    TransformedTable = #"Your Transformed Table",
    ColumnsToCheck = {"CustomerID", "OrderDate", "TotalAmount"},
    
    // Function to count nulls in a column
    CountNulls = (tbl as table, colName as text) =>
        let
            Column = Table.Column(tbl, colName),
            NullCount = List.Count(List.Select(Column, each _ = null))
        in
            NullCount,
    
    // Check each column
    Results = List.Transform(
        ColumnsToCheck,
        (col) => 
            let
                NullCount = CountNulls(TransformedTable, col),
                Status = if NullCount = 0 
                        then "✅ PASS" 
                        else "⚠️ WARN: " & Number.ToText(NullCount) & " nulls"
            in
                {col, NullCount, Status}
    ),
    
    ResultTable = #table(
        {"ColumnName", "NullCount", "Status"},
        Results
    )
in
    ResultTable


// ============================================================
// 4. SUM VALIDATION
// ============================================================
// Compare sum of numeric column between source and transformed
let
    SourceTable = #"Your Source Table",
    TransformedTable = #"Your Transformed Table",
    ColumnToValidate = "TotalAmount",
    
    SourceSum = List.Sum(Table.Column(SourceTable, ColumnToValidate)),
    TransformedSum = List.Sum(Table.Column(TransformedTable, ColumnToValidate)),
    Difference = TransformedSum - SourceSum,
    
    ValidationStatus = if Difference = 0 
                       then "✅ PASS: Sums match"
                       else "⚠️ WARN: Difference of " & Number.ToText(Difference),
    
    Result = #table(
        {"Column", "SourceSum", "TransformedSum", "Difference", "Status"},
        {{ColumnToValidate, SourceSum, TransformedSum, Difference, ValidationStatus}}
    )
in
    Result


// ============================================================
// 5. DUPLICATE CHECK
// ============================================================
// Check for duplicates in key column
let
    TransformedTable = #"Your Transformed Table",
    KeyColumn = "CustomerID",
    
    // Group by key column and count occurrences
    Grouped = Table.Group(
        TransformedTable, 
        {KeyColumn}, 
        {{"Count", each Table.RowCount(_), Int64.Type}}
    ),
    
    // Filter to find duplicates
    Duplicates = Table.SelectRows(Grouped, each [Count] > 1),
    DuplicateCount = Table.RowCount(Duplicates),
    
    ValidationStatus = if DuplicateCount = 0 
                       then "✅ PASS: No duplicates found"
                       else "❌ FAIL: " & Number.ToText(DuplicateCount) & " duplicate values",
    
    Result = #table(
        {"Test", "KeyColumn", "DuplicateCount", "Status"},
        {{"Duplicate Check", KeyColumn, DuplicateCount, ValidationStatus}}
    )
in
    Result


// ============================================================
// 6. DATA TYPE VALIDATION
// ============================================================
// Verify data types of columns
let
    TransformedTable = #"Your Transformed Table",
    ExpectedTypes = {
        {"CustomerID", type number},
        {"CustomerName", type text},
        {"OrderDate", type datetime},
        {"TotalAmount", type number}
    },
    
    ActualTypes = Table.Schema(TransformedTable),
    
    ValidationResults = List.Transform(
        ExpectedTypes,
        (expected) =>
            let
                ColName = expected{0},
                ExpectedType = expected{1},
                ActualRow = Table.SelectRows(ActualTypes, each [Name] = ColName),
                ActualType = if Table.RowCount(ActualRow) > 0 
                            then ActualRow{0}[Kind] 
                            else "Column Not Found",
                Status = if ActualType = Type.ToText(ExpectedType)
                        then "✅ PASS"
                        else "❌ FAIL"
            in
                {ColName, Type.ToText(ExpectedType), ActualType, Status}
    ),
    
    Result = #table(
        {"Column", "ExpectedType", "ActualType", "Status"},
        ValidationResults
    )
in
    Result


// ============================================================
// 7. DATE RANGE VALIDATION
// ============================================================
// Validate date column is within expected range
let
    TransformedTable = #"Your Transformed Table",
    DateColumn = "OrderDate",
    ExpectedMinDate = #date(2020, 1, 1),
    ExpectedMaxDate = #date(2024, 12, 31),
    
    Dates = Table.Column(TransformedTable, DateColumn),
    ActualMinDate = List.Min(Dates),
    ActualMaxDate = List.Max(Dates),
    
    MinDateValid = ActualMinDate >= ExpectedMinDate,
    MaxDateValid = ActualMaxDate <= ExpectedMaxDate,
    
    ValidationStatus = if MinDateValid and MaxDateValid 
                       then "✅ PASS: All dates within range"
                       else "❌ FAIL: Dates outside expected range",
    
    Result = #table(
        {"Test", "ExpectedMin", "ActualMin", "ExpectedMax", "ActualMax", "Status"},
        {{"Date Range", Date.ToText(ExpectedMinDate), Date.ToText(ActualMinDate), 
          Date.ToText(ExpectedMaxDate), Date.ToText(ActualMaxDate), ValidationStatus}}
    )
in
    Result


// ============================================================
// 8. COMPREHENSIVE VALIDATION DASHBOARD
// ============================================================
// Combine multiple validation checks into one table
let
    // Define your tables
    SourceTable = #"Your Source Table",
    TransformedTable = #"Your Transformed Table",
    
    // Row count check
    RowCountCheck = {
        "Row Count",
        if Table.RowCount(SourceTable) = Table.RowCount(TransformedTable) 
        then "✅ PASS" 
        else "❌ FAIL",
        "Source: " & Number.ToText(Table.RowCount(SourceTable)) & ", Transformed: " & Number.ToText(Table.RowCount(TransformedTable))
    },
    
    // Column count check
    ColumnCountCheck = {
        "Column Count",
        if List.Count(Table.ColumnNames(SourceTable)) <= List.Count(Table.ColumnNames(TransformedTable))
        then "✅ PASS"
        else "⚠️ WARN",
        "Source: " & Number.ToText(List.Count(Table.ColumnNames(SourceTable))) & ", Transformed: " & Number.ToText(List.Count(Table.ColumnNames(TransformedTable)))
    },
    
    // Null check example
    NullCheck = {
        "Null Values",
        "✅ PASS",
        "No critical nulls found"
    },
    
    // Combine all checks
    AllChecks = {RowCountCheck, ColumnCountCheck, NullCheck},
    
    Result = #table(
        {"Validation Test", "Status", "Details"},
        AllChecks
    )
in
    Result


// ============================================================
// USAGE INSTRUCTIONS
// ============================================================
// 1. Copy the relevant validation query above
// 2. In Power BI Desktop, go to Home > Transform Data
// 3. In Power Query Editor, click Home > New Source > Blank Query
// 4. Click Advanced Editor and paste the M code
// 5. Replace "Your Source Table" and "Your Transformed Table" with your actual table names
// 6. Rename the query to something like "Validation_RowCount"
// 7. Right-click the query and UNCHECK "Enable Load" (don't load to model)
// 8. Click Close & Apply
// 9. During development, open Power Query Editor to check validation results
// ============================================================
