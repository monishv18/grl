import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "./collapsible";
import { ChevronDown, FileText, CheckCircle, AlertCircle, Info } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "./badge";

interface ParsedData {
  [key: string]: any;
}

interface ResultDisplayProps {
  data: ParsedData;
  fileName: string;
  className?: string;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({
  data,
  fileName,
  className,
}) => {
  const [openSections, setOpenSections] = React.useState<Set<string>>(new Set(["overview"]));

  const toggleSection = (section: string) => {
    const newOpenSections = new Set(openSections);
    if (newOpenSections.has(section)) {
      newOpenSections.delete(section);
    } else {
      newOpenSections.add(section);
    }
    setOpenSections(newOpenSections);
  };

  const renderValue = (value: any, depth = 0): React.ReactNode => {
    if (value === null || value === undefined) {
      return <span className="text-muted-foreground italic">No data</span>;
    }

    if (typeof value === "boolean") {
      return (
        <Badge variant={value ? "default" : "secondary"}>
          {value ? "Yes" : "No"}
        </Badge>
      );
    }

    if (typeof value === "string" || typeof value === "number") {
      return <span className="text-foreground">{value}</span>;
    }

    if (Array.isArray(value)) {
      if (value.length === 0) {
        return <span className="text-muted-foreground italic">Empty list</span>;
      }
      return (
        <ul className="space-y-1 mt-2">
          {value.map((item, index) => (
            <li key={index} className="flex items-start space-x-2">
              <span className="text-muted-foreground">•</span>
              <div>{renderValue(item, depth + 1)}</div>
            </li>
          ))}
        </ul>
      );
    }

    if (typeof value === "object") {
      return (
        <div className={cn("space-y-2", depth > 0 && "mt-2 ml-4 pl-4 border-l border-border")}>
          {Object.entries(value).map(([key, val]) => (
            <div key={key} className="space-y-1">
              <dt className="text-sm font-medium text-muted-foreground capitalize">
                {key.replace(/([A-Z])/g, " $1").replace(/^./, (str) => str.toUpperCase())}
              </dt>
              <dd className="text-sm">{renderValue(val, depth + 1)}</dd>
            </div>
          ))}
        </div>
      );
    }

    return <span className="text-foreground">{String(value)}</span>;
  };

  const getSectionIcon = (key: string) => {
    const iconMap: { [key: string]: React.ReactNode } = {
      overview: <FileText className="w-4 h-4" />,
      validation: <CheckCircle className="w-4 h-4" />,
      errors: <AlertCircle className="w-4 h-4" />,
      metadata: <Info className="w-4 h-4" />,
    };
    return iconMap[key.toLowerCase()] || <FileText className="w-4 h-4" />;
  };

  const getSectionVariant = (key: string) => {
    if (key.toLowerCase().includes("error")) return "destructive";
    if (key.toLowerCase().includes("validation")) return "success";
    return "default";
  };

  return (
    <div className={cn("space-y-4", className)}>
      <Card className="slide-up">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-primary" />
            <span>Processing Results</span>
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            Results for: <span className="font-medium">{fileName}</span>
          </p>
        </CardHeader>
      </Card>

      <div className="space-y-3">
        {Object.entries(data).map(([key, value]) => {
          const sectionKey = key.toLowerCase();
          const isOpen = openSections.has(sectionKey);
          const variant = getSectionVariant(key);

          return (
            <Card key={key} className="slide-up">
              <Collapsible
                open={isOpen}
                onOpenChange={() => toggleSection(sectionKey)}
              >
                <CollapsibleTrigger asChild>
                  <CardHeader className="cursor-pointer hover:bg-muted/50 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className={cn(
                          "w-8 h-8 rounded-lg flex items-center justify-center",
                          variant === "destructive" && "bg-destructive/10 text-destructive",
                          variant === "success" && "bg-success/10 text-success",
                          variant === "default" && "bg-primary/10 text-primary"
                        )}>
                          {getSectionIcon(key)}
                        </div>
                        <CardTitle className="text-lg capitalize">
                          {key.replace(/([A-Z])/g, " $1").replace(/^./, (str) => str.toUpperCase())}
                        </CardTitle>
                      </div>
                      <ChevronDown
                        className={cn(
                          "w-5 h-5 transition-transform duration-200",
                          isOpen && "rotate-180"
                        )}
                      />
                    </div>
                  </CardHeader>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <CardContent className="pt-0">
                    <div className="space-y-3">
                      {renderValue(value)}
                    </div>
                  </CardContent>
                </CollapsibleContent>
              </Collapsible>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default ResultDisplay;